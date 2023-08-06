from __future__ import print_function, unicode_literals

import os, re
from base64 import b64encode, b64decode

from eight import *
from lxml import etree
from lxml.etree import Element, SubElement
from defusedxml.lxml import fromstring

import cryptography.exceptions
from cryptography.hazmat.primitives.asymmetric import rsa, dsa, ec
from cryptography.hazmat.primitives.asymmetric.padding import PKCS1v15
from cryptography.hazmat.primitives.hashes import Hash, SHA1, SHA224, SHA256, SHA384, SHA512
from cryptography.hazmat.backends import default_backend

from .util import bytes_to_long, long_to_bytes, strip_pem_header, add_pem_header

XMLDSIG_NS = "http://www.w3.org/2000/09/xmldsig#"
XMLDSIG11_NS = "http://www.w3.org/2009/xmldsig11#"
XMLENC_NS = "http://www.w3.org/2001/04/xmlenc#"
XMLDSIG_MORE_NS = "http://www.w3.org/2001/04/xmldsig-more#"

namespaces = dict(ds=XMLDSIG_NS, ds11=XMLDSIG11_NS)

def ds_tag(tag):
    return "{" + XMLDSIG_NS + "}" + tag

def ds11_tag(tag):
    return "{" + XMLDSIG11_NS + "}" + tag

class InvalidSignature(cryptography.exceptions.InvalidSignature):
    """
    Raised when signature validation fails.
    """

class InvalidCertificate(InvalidSignature):
    """
    Raised when certificate validation fails.
    """

class InvalidInput(ValueError):
    pass

_schema = None

# Note: This regexp is a very ugly way to process XML data, but it's mandated by the standard, which requires that the
# signature be excised after c14n, leaving behind extra whitespace that needs to be part of the digest.
def _get_signature_regex(ns_prefix=None):
    tag = "Signature"
    if ns_prefix is not None:
        tag = ns_prefix + ":" + tag
    return re.compile(bytes('<{t}[>\s].*?</{t}>'.format(t=tag)), flags=re.DOTALL)

def _get_schema():
    global _schema
    if _schema is None:
        schema_file = os.path.join(os.path.dirname(__file__), "schemas", "xmldsig1-schema.xsd")
        with open(schema_file) as fh:
            _schema = etree.XMLSchema(etree.parse(fh))
    return _schema

class xmldsig(object):
    """
    Create a new XML Signature object. This is the main entry point to the functionality of the module.

    :param data: Data to sign, or signature data to verify
    :type data: String or XML ElementTree Element API compatible object
    :param digest_algorithm: Digest algorithm that will be used to hash the data during signature generation
    :type digest_algorithm: string
    """
    def __init__(self, data, digest_algorithm="sha256"):
        self.digest_alg = digest_algorithm
        self.signature_alg = None
        self.data = data

    known_digest_methods = {
        XMLDSIG_NS + "sha1": SHA1,
        XMLENC_NS + "sha256": SHA256,
        XMLDSIG_MORE_NS + "sha224": SHA224,
        XMLDSIG_MORE_NS + "sha384": SHA384,
        XMLENC_NS + "sha512": SHA512,
    }

    known_hmac_digest_methods = {
        XMLDSIG_NS + "hmac-sha1": SHA1,
        XMLDSIG_MORE_NS + "hmac-sha256": SHA256,
        XMLDSIG_MORE_NS + "hmac-sha384": SHA384,
        XMLDSIG_MORE_NS + "hmac-sha512": SHA512,
        XMLDSIG_MORE_NS + "hmac-sha224": SHA224,
    }

    known_signature_digest_methods = {
        XMLDSIG_MORE_NS + "rsa-sha256": SHA256,
        XMLDSIG_MORE_NS + "ecdsa-sha256": SHA256,
        XMLDSIG_NS + "dsa-sha1": SHA1,
        XMLDSIG_NS + "rsa-sha1": SHA1,
        XMLDSIG_MORE_NS + "rsa-sha224": SHA224,
        XMLDSIG_MORE_NS + "rsa-sha384": SHA384,
        XMLDSIG_MORE_NS + "rsa-sha512": SHA512,
        XMLDSIG_MORE_NS + "ecdsa-sha1": SHA1,
        XMLDSIG_MORE_NS + "ecdsa-sha224": SHA224,
        XMLDSIG_MORE_NS + "ecdsa-sha384": SHA384,
        XMLDSIG_MORE_NS + "ecdsa-sha512": SHA512,
        XMLDSIG11_NS + "dsa-sha256": SHA256,
    }
    known_digest_tags = {method.split("#")[1]: method for method in known_digest_methods}
    known_hmac_digest_tags = {method.split("#")[1]: method for method in known_hmac_digest_methods}
    known_signature_digest_tags = {method.split("#")[1]: method for method in known_signature_digest_methods}

    # See https://tools.ietf.org/html/rfc5656
    known_ecdsa_curves = {
        "urn:oid:1.2.840.10045.3.1.7": ec.SECP256R1,
        "urn:oid:1.3.132.0.34": ec.SECP384R1,
        "urn:oid:1.3.132.0.35": ec.SECP521R1,
        "urn:oid:1.3.132.0.1": ec.SECT163K1,
        "urn:oid:1.2.840.10045.3.1.1": ec.SECP192R1,
        "urn:oid:1.3.132.0.33": ec.SECP224R1,
        "urn:oid:1.3.132.0.26": ec.SECT233K1,
        "urn:oid:1.3.132.0.27": ec.SECT233R1,
        "urn:oid:1.3.132.0.16": ec.SECT283R1,
        "urn:oid:1.3.132.0.36": ec.SECT409K1,
        "urn:oid:1.3.132.0.37": ec.SECT409R1,
        "urn:oid:1.3.132.0.38": ec.SECT571K1,
    }
    known_ecdsa_curve_oids = {ec().name: oid for oid, ec in known_ecdsa_curves.iteritems()}

    def _get_digest(self, data, digest_algorithm):
        hasher = Hash(algorithm=digest_algorithm, backend=default_backend())
        hasher.update(data)
        return b64encode(hasher.finalize())

    def _get_digest_method(self, digest_algorithm_id, methods=None):
        if methods is None:
            methods = self.known_digest_methods
        if digest_algorithm_id not in methods:
            raise InvalidInput('Algorithm "{}" is not recognized'.format(digest_algorithm_id))
        return methods[digest_algorithm_id]()

    def _get_digest_method_by_tag(self, digest_algorithm_tag, methods=None, known_tags=None):
        if known_tags is None:
            known_tags = self.known_digest_tags
        if digest_algorithm_tag not in known_tags:
            raise InvalidInput('Algorithm tag "{}" is not recognized'.format(digest_algorithm_tag))
        return self._get_digest_method(known_tags[digest_algorithm_tag], methods=methods)

    def _get_hmac_digest_method(self, hmac_algorithm_id):
        return self._get_digest_method(hmac_algorithm_id, methods=self.known_hmac_digest_methods)

    def _get_hmac_digest_method_by_tag(self, hmac_algorithm_tag):
        return self._get_digest_method_by_tag(hmac_algorithm_tag, methods=self.known_hmac_digest_methods,
                                              known_tags=self.known_hmac_digest_tags)

    def _get_signature_digest_method(self, signature_algorithm_id):
        return self._get_digest_method(signature_algorithm_id, methods=self.known_signature_digest_methods)

    def _get_signature_digest_method_by_tag(self, signature_algorithm_tag):
        return self._get_digest_method_by_tag(signature_algorithm_tag, methods=self.known_signature_digest_methods,
                                              known_tags=self.known_signature_digest_tags)

    def _get_payload_c14n(self, enveloped, with_comments):
        if enveloped:
            self.payload = self.data
            if isinstance(self.data, (str, bytes)):
                raise InvalidInput("When using enveloped signature, **data** must be an XML element")

            signature_placeholders = self._findall(self.data, "Signature[@Id='placeholder']")

            if len(signature_placeholders) == 0:
                self.sig_root = Element(ds_tag("Signature"), nsmap=dict(ds=XMLDSIG_NS))
                self.payload.append(self.sig_root)
            elif len(signature_placeholders) == 1:
                self.sig_root = signature_placeholders[0]
                del self.sig_root.attrib["Id"]
            else:
                raise InvalidInput("Enveloped signature input contains more than one placeholder")

            self._reference_uri = ""
        else:
            self.sig_root = Element(ds_tag("Signature"), nsmap=dict(ds=XMLDSIG_NS))
            self.payload = Element(ds_tag("Object"), nsmap=dict(ds=XMLDSIG_NS), Id="object")
            self._reference_uri = "#object"
            if isinstance(self.data, (str, bytes)):
                self.payload.text = self.data
            else:
                self.payload.append(self.data)

        self.payload_c14n = self._c14n(self.payload, with_comments=with_comments,
                                       inclusive_ns_prefixes=self.sig_root.nsmap.keys())
        if enveloped:
            self.payload_c14n = _get_signature_regex(ns_prefix="ds").sub(b"", self.payload_c14n)

    def _serialize_key_value(self, key, key_info_element):
        key_value = SubElement(key_info_element, ds_tag("KeyValue"))
        if self.signature_alg.startswith("rsa-"):
            rsa_key_value = SubElement(key_value, ds_tag("RSAKeyValue"))
            modulus = SubElement(rsa_key_value, ds_tag("Modulus"))
            modulus.text = b64encode(long_to_bytes(key.public_key().public_numbers().n))
            exponent = SubElement(rsa_key_value, ds_tag("Exponent"))
            exponent.text = b64encode(long_to_bytes(key.public_key().public_numbers().e))
        elif self.signature_alg.startswith("dsa-"):
            dsa_key_value = SubElement(key_value, ds_tag("DSAKeyValue"))
            for field in "p", "q", "g", "y":
                e = SubElement(dsa_key_value, ds_tag(field.upper()))

                if field == "y":
                    key_params = key.public_key().public_numbers()
                else:
                    key_params = key.parameters().parameter_numbers()

                e.text = b64encode(long_to_bytes(getattr(key_params, field)))
        elif self.signature_alg.startswith("ecdsa-"):
            ec_key_value = SubElement(key_value, ds11_tag("ECKeyValue"), nsmap=dict(ds11=XMLDSIG11_NS))
            named_curve = SubElement(ec_key_value, ds11_tag("NamedCurve"), URI=self.known_ecdsa_curve_oids[key.curve.name])
            public_key = SubElement(ec_key_value, ds11_tag("PublicKey"))
            x = key.public_key().public_numbers().x
            y = key.public_key().public_numbers().y
            public_key.text = b64encode(long_to_bytes(4) + long_to_bytes(x) + long_to_bytes(y))

    def _c14n(self, node, with_comments=True, inclusive_ns_prefixes=None):
        if inclusive_ns_prefixes is None:
            inclusive_ns_prefixes = []
        return etree.tostring(node, method="c14n", exclusive=True, with_comments=with_comments,
                              inclusive_ns_prefixes=[p for p in inclusive_ns_prefixes if p is not None])

    def sign(self, algorithm="rsa-sha256", key=None, passphrase=None, cert=None, with_comments=False, enveloped=True):
        """
        Sign the data and return the root element of the resulting XML tree.

        :param algorithm: Algorithm that will be used to generate the signature, composed of the signature algorithm and the digest algorithm, separated by a hyphen. All algorthm IDs listed under the `Algorithm Identifiers and Implementation Requirements <http://www.w3.org/TR/xmldsig-core1/#sec-AlgID>`_ section of the XML Signature 1.1 standard are supported.
        :type algorithm: string
        :param key: Key to be used for signing. When signing with a certificate or RSA/DSA/ECDSA key, this can be a string containing a PEM-formatted key, or a :py:class:`cryptography.hazmat.primitives.interfaces.RSAPublicKey`, :py:class:`cryptography.hazmat.primitives.interfaces.DSAPublicKey`, or :py:class:`cryptography.hazmat.primitives.interfaces.EllipticCurvePublicKey` object. When signing with a HMAC, this should be a string containing the shared secret.
        :type key: string, :py:class:`cryptography.hazmat.primitives.interfaces.RSAPublicKey`, :py:class:`cryptography.hazmat.primitives.interfaces.DSAPublicKey`, or :py:class:`cryptography.hazmat.primitives.interfaces.EllipticCurvePublicKey` object
        :param passphrase: Passphrase to use to decrypt the key, if any.
        :type passphrase: string
        :param cert: X.509 certificate to use for signing. This should be a string containing a PEM-formatted certificate, or an array containing the certificate and a chain of intermediate certificates.
        :type cert: string or array of strings
        :param with_comments: Whether to canonicalize (c14n) the payload with comments or without.
        :type with_comments: boolean
        :param enveloped: If `True`, the enveloped signature signing method will be used. If `False`, the enveloping signature method will be used.
        :type enveloped: boolean

        :returns: A :py:class:`lxml.etree.Element` object representing the root of the XML tree containing the signature and the payload data.

        To specify the location of an enveloped signature within **data**, insert a `<Signature Id="placeholder"></Signature>`
        element in **data**. This element will be replaced by the generated signature, and excised when generating the digest.
        """
        self.signature_alg = algorithm
        self.key = key

        if isinstance(cert, (str, bytes)):
            cert_chain = [cert]
        else:
            cert_chain = cert

        self._get_payload_c14n(enveloped, with_comments)

        self.digest = self._get_digest(self.payload_c14n, self._get_digest_method_by_tag(self.digest_alg))

        signed_info = SubElement(self.sig_root, ds_tag("SignedInfo"), nsmap=dict(ds=XMLDSIG_NS))
        c14n_algorithm = "http://www.w3.org/2006/12/xml-c14n11"
        if with_comments:
            c14n_algorithm += "#WithComments"
        c14n_method = SubElement(signed_info, ds_tag("CanonicalizationMethod"), Algorithm=c14n_algorithm)
        if self.signature_alg.startswith("hmac-"):
            algorithm_id = self.known_hmac_digest_tags[self.signature_alg]
        else:
            algorithm_id = self.known_signature_digest_tags[self.signature_alg]
        signature_method = SubElement(signed_info, ds_tag("SignatureMethod"), Algorithm=algorithm_id)
        reference = SubElement(signed_info, ds_tag("Reference"), URI=self._reference_uri)
        if enveloped:
            transforms = SubElement(reference, ds_tag("Transforms"))
            SubElement(transforms, ds_tag("Transform"), Algorithm=XMLDSIG_NS + "enveloped-signature")
        digest_method = SubElement(reference, ds_tag("DigestMethod"), Algorithm=self.known_digest_tags[self.digest_alg])
        digest_value = SubElement(reference, ds_tag("DigestValue"))
        digest_value.text = self.digest
        signature_value = SubElement(self.sig_root, ds_tag("SignatureValue"))

        signed_info_c14n = self._c14n(signed_info)
        if self.signature_alg.startswith("hmac-"):
            from cryptography.hazmat.primitives.hmac import HMAC
            signer = HMAC(key=self.key,
                          algorithm=self._get_hmac_digest_method_by_tag(self.signature_alg),
                          backend=default_backend())
            signer.update(signed_info_c14n)
            signature_value.text = b64encode(signer.finalize())
            self.sig_root.append(signature_value)
        elif self.signature_alg.startswith("dsa-") or self.signature_alg.startswith("rsa-") or self.signature_alg.startswith("ecdsa-"):
            if isinstance(self.key, (str, bytes)):
                from cryptography.hazmat.primitives.serialization import load_pem_private_key
                key = load_pem_private_key(self.key, password=passphrase, backend=default_backend())
            else:
                key = self.key

            hash_alg = self._get_signature_digest_method_by_tag(self.signature_alg)
            if self.signature_alg.startswith("dsa-"):
                signer = key.signer(algorithm=hash_alg)
            elif self.signature_alg.startswith("ecdsa-"):
                signer = key.signer(signature_algorithm=ec.ECDSA(algorithm=hash_alg))
            elif self.signature_alg.startswith("rsa-"):
                signer = key.signer(padding=PKCS1v15(), algorithm=hash_alg)
            else:
                raise NotImplementedError()
            signer.update(signed_info_c14n)
            signature = signer.finalize()
            if self.signature_alg.startswith("dsa-"):
                # Note: The output of the DSA signer is a DER-encoded ASN.1 sequence of two DER integers.
                # Bytes 0-1: DER sequence header and length
                # Bytes 2-3: DER integer header and length (r_len)
                # Bytes 4-4+r_len-1: r (first half of DSA signature)
                # Bytes 4+r_len-5+r_len: DER integer header and length
                # Bytes 6+r_len to the end: s (second half of DSA signature)
                r_len = bytes_to_long(signature[3])
                r, s = signature[4:4+r_len], signature[6+r_len:]
                signature = r.rjust(32, b"\0") + s.rjust(32, b"\0")
            signature_value.text = b64encode(signature)

            key_info = SubElement(self.sig_root, ds_tag("KeyInfo"))
            if cert_chain is None:
                self._serialize_key_value(key, key_info)
            else:
                x509_data = SubElement(key_info, ds_tag("X509Data"))
                for cert in cert_chain:
                    x509_certificate = SubElement(x509_data, ds_tag("X509Certificate"))
                    if isinstance(cert, (str, bytes)):
                        x509_certificate.text = strip_pem_header(cert)
                    else:
                        from OpenSSL.crypto import dump_certificate, FILETYPE_PEM
                        print("BEGIN DUMP")
                        print(dump_certificate(FILETYPE_PEM, cert))
                        print("END DUMP")
                        x509_certificate.text = dump_certificate(FILETYPE_PEM, cert)
        else:
            raise NotImplementedError()

        if enveloped:
            return self.payload
        else:
            self.sig_root.append(self.payload)
            return self.sig_root

    def _verify_signature_with_pubkey(self, signed_info_c14n, raw_signature, key_value, signature_alg):
        if "ecdsa-" in signature_alg:
            ec_key_value = self._find(key_value, "ECKeyValue", namespace="ds11")
            named_curve = self._find(ec_key_value, "NamedCurve", namespace="ds11")
            public_key = self._find(ec_key_value, "PublicKey", namespace="ds11")
            key_data = b64decode(public_key.text)[1:]
            x = bytes_to_long(key_data[:len(key_data)/2])
            y = bytes_to_long(key_data[len(key_data)/2:])
            curve_class = self.known_ecdsa_curves[named_curve.get("URI")]
            key = ec.EllipticCurvePublicNumbers(x=x, y=y, curve=curve_class()).public_key(backend=default_backend())
            verifier = key.verifier(raw_signature, ec.ECDSA(self._get_signature_digest_method(signature_alg)))
        elif "dsa-" in signature_alg:
            dsa_key_value = self._find(key_value, "DSAKeyValue")
            p = self._get_long(dsa_key_value, "P")
            q = self._get_long(dsa_key_value, "Q")
            g = self._get_long(dsa_key_value, "G", require=False)
            y = self._get_long(dsa_key_value, "Y")
            pn = dsa.DSAPublicNumbers(y=y, parameter_numbers=dsa.DSAParameterNumbers(p=p, q=q, g=g))
            key = pn.public_key(backend=default_backend())
            def as_der_sequence(r, s):
                return long_to_bytes(0x30) + long_to_bytes(len(r) + len(s)) + r + s
            def as_der_integer(i):
                return long_to_bytes(0x02) + long_to_bytes(len(i)) + i
            sig_as_der_seq = as_der_sequence(as_der_integer(raw_signature[:len(raw_signature)/2]),
                                             as_der_integer(raw_signature[len(raw_signature)/2:]))
            verifier = key.verifier(sig_as_der_seq, self._get_signature_digest_method(signature_alg))
        elif "rsa-" in signature_alg:
            rsa_key_value = self._find(key_value, "RSAKeyValue")
            modulus = self._get_long(rsa_key_value, "Modulus")
            exponent = self._get_long(rsa_key_value, "Exponent")
            key = rsa.RSAPublicNumbers(e=exponent, n=modulus).public_key(backend=default_backend())
            verifier = key.verifier(raw_signature, padding=PKCS1v15(), algorithm=self._get_signature_digest_method(signature_alg))
        else:
            raise NotImplementedError()

        verifier.update(signed_info_c14n)
        verifier.verify()

    def verify(self, require_x509=True, x509_cert=None, ca_pem_file=None, ca_path=None, hmac_key=None, validate_schema=True, parser=None):
        """
        Verify the XML signature supplied in the data, or raise an exception. By default, this requires the signature to
        be generated using a valid X.509 certificate. To enable other means of signature validation, set the
        **require_x509** argument to `False`.

        TODO: CN verification

        :param require_x509: If ``True``, a valid X.509 certificate-based signature is required to pass validation. If ``False``, other types of valid signatures (e.g. HMAC or RSA public key) are accepted.
        :type require_x509: boolean
        :param x509_cert: An external X.509 certificate, given as a PEM-formatted string, to use for verification. Overrides any X.509 certificate information supplied by the signature. If left set to ``None``, requires that the signature supply a valid X.509 certificate chain that validates against the known certificate authorities. Implies **require_x509=True**.
        :type x509_cert: string
        :param ca_pem_file: Filename (as bytes) of a PEM file containing certificate authority information to use when verifying certificate-based signatures.
        :type ca_pem_file: bytes
        :param ca_path: Path to a directory containing PEM-formatted certificate authority files to use when verifying certificate-based signatures. If neither **ca_pem_file** nor **ca_path** is given, the Mozilla CA bundle provided by :py:mod:`certifi` will be loaded.
        :type ca_path: string
        :param hmac_key: If using HMAC, a string containing the shared secret.
        :type hmac_key: string
        :param validate_schema: Whether to validate **data** against the XML Signature schema.
        :type validate_schema: boolean
        :param parser: Custom XML parser instance to use when parsing **data**.
        :type parser: :py:class:`ElementTree.XMLParser` compatible parser

        :raises: :py:class:`cryptography.exceptions.InvalidSignature`
        """
        self.hmac_key = hmac_key
        self.require_x509 = require_x509
        self.x509_cert = x509_cert
        if x509_cert:
            self.require_x509 = True

        if isinstance(self.data, (str, bytes)):
            root = fromstring(self.data, parser=parser)
        else:
            root = self.data

        if root.tag == ds_tag("Signature"):
            enveloped = False
            signature = root
        else:
            enveloped = True
            signature = self._find(root, "Signature")

        if validate_schema:
            _get_schema().assertValid(signature)

        signed_info = self._find(signature, "SignedInfo")
        c14n_method = self._find(signed_info, "CanonicalizationMethod")
        if c14n_method.get("Algorithm").endswith("#WithComments"):
            with_comments = True
        else:
            with_comments = False
        signed_info_c14n = self._c14n(signed_info, with_comments=with_comments, inclusive_ns_prefixes=root.nsmap.keys())
        reference = self._find(signed_info, "Reference")
        digest_algorithm = self._find(reference, "DigestMethod").get("Algorithm")
        digest_value = self._find(reference, "DigestValue")

        if enveloped:
            payload = root
        else:
            payload = self._find(signature, 'Object[@Id="{}"]'.format(reference.get("URI").lstrip("#")))

        payload_c14n = self._c14n(payload, with_comments=with_comments, inclusive_ns_prefixes=root.nsmap.keys())

        if enveloped:
            payload_c14n = _get_signature_regex(ns_prefix=signature.prefix).sub(b"", payload_c14n)

        if digest_value.text != self._get_digest(payload_c14n, self._get_digest_method(digest_algorithm)):
            raise InvalidSignature("Digest mismatch")

        signature_method = self._find(signed_info, "SignatureMethod")
        signature_value = self._find(signature, "SignatureValue")
        signature_alg = signature_method.get("Algorithm")
        raw_signature = b64decode(signature_value.text)
        x509_data = signature.find("ds:KeyInfo/ds:X509Data", namespaces=namespaces)

        if x509_data is not None or self.require_x509:
            from OpenSSL.crypto import load_certificate, FILETYPE_PEM, verify

            if self.x509_cert is None:
                if x509_data is None:
                    raise InvalidInput("Expected a X.509 certificate based signature")
                certs = [cert.text for cert in self._findall(x509_data, "X509Certificate")]
                cert_chain = [load_certificate(FILETYPE_PEM, add_pem_header(cert)) for cert in certs]
                verify_x509_cert_chain(cert_chain, ca_pem_file=ca_pem_file, ca_path=ca_path)
            else:
                cert_chain = [load_certificate(FILETYPE_PEM, add_pem_header(self.x509_cert))]

            signature_digest_method = self._get_signature_digest_method(signature_alg).name
            verify(cert_chain[-1], raw_signature, signed_info_c14n, bytes(signature_digest_method))
        elif "hmac-sha" in signature_alg:
            if self.hmac_key is None:
                raise InvalidInput('Parameter "hmac_key" is required when verifying a HMAC signature')

            from cryptography.hazmat.primitives.hmac import HMAC
            signer = HMAC(key=bytes(self.hmac_key),
                          algorithm=self._get_hmac_digest_method(signature_alg),
                          backend=default_backend())
            signer.update(signed_info_c14n)
            if raw_signature != signer.finalize():
                raise InvalidSignature("Signature mismatch (HMAC)")
        else:
            key_value = signature.find("ds:KeyInfo/ds:KeyValue", namespaces=namespaces)
            if key_value is None:
                raise InvalidInput("Expected to find either KeyValue or X509Data XML element in KeyInfo")

            self._verify_signature_with_pubkey(signed_info_c14n, raw_signature, key_value, signature_alg)

    def _get_long(self, element, query, require=True):
        result = self._find(element, query, require=require)
        if result is not None:
            result = bytes_to_long(b64decode(result.text))
        return result

    def _find(self, element, query, require=True, namespace="ds"):
        result = element.find(namespace + ":" + query, namespaces=namespaces)
        if require and result is None:
            raise InvalidInput("Expected to find XML element {} in {}".format(query, element.tag))
        return result

    def _findall(self, element, query, namespace="ds"):
        return element.findall(namespace + ":" + query, namespaces=namespaces)

def verify_x509_cert_chain(cert_chain, ca_pem_file=None, ca_path=None):
    from OpenSSL import SSL, crypto
    context = SSL.Context(SSL.TLSv1_METHOD)
    if ca_pem_file is None and ca_path is None:
        import certifi
        ca_pem_file = certifi.where()
    context.load_verify_locations(ca_pem_file, capath=ca_path)
    store = context.get_cert_store()
    for cert in cert_chain:
        # The following certificate chain verification code uses an internal pyOpenSSL API with guidance from
        # https://github.com/pyca/pyopenssl/pull/155
        # TODO: Update this to use the public API once the PR lands.
        store_ctx = SSL._lib.X509_STORE_CTX_new()
        _store_ctx = SSL._ffi.gc(store_ctx, SSL._lib.X509_STORE_CTX_free)
        SSL._lib.X509_STORE_CTX_init(store_ctx, store._store, cert._x509, SSL._ffi.NULL)
        result = SSL._lib.X509_verify_cert(_store_ctx)
        SSL._lib.X509_STORE_CTX_cleanup(_store_ctx)
        if result <= 0:
            e = SSL._lib.X509_STORE_CTX_get_error(_store_ctx)
            msg = SSL._ffi.string(SSL._lib.X509_verify_cert_error_string(e))
            raise InvalidCertificate(msg)
        else:
            try:
                store.add_cert(cert)
            except crypto.Error as e:
                if e.args == ([('x509 certificate routines', 'X509_STORE_add_cert', 'cert already in hash table')],):
                    continue
                else:
                    raise
