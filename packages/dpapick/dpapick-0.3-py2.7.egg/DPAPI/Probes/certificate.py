#!/usr/bin/env python
# -*- coding: utf-8 -*-

# ############################################################################
##                                                                         ##
## This file is part of DPAPIck                                            ##
## Windows DPAPI decryption & forensic toolkit                             ##
##                                                                         ##
##                                                                         ##
## Copyright (C) 2010, 2011 Cassidian SAS. All rights reserved.            ##
## This document is the property of Cassidian SAS, it may not be copied or ##
## circulated without prior licence                                        ##
##                                                                         ##
##  Author: Jean-Michel Picod <jmichel.p@gmail.com>                        ##
##                                                                         ##
## This program is distributed under GPLv3 licence (see LICENCE.txt)       ##
##                                                                         ##
#############################################################################

from DPAPI import probe
from DPAPI.Core import blob

try:
    from pyasn1.type import univ, namedtype
    from pyasn1.codec.der import encoder
except:
    raise Exception("PyASN1 is required.")


class PrivateKeyBlob(probe.DPAPIProbe):
    """This class represents a RSA private key file as used by Internet Explorer
    and EFS certificates.
    They are located under %APPDATA%\\Microsoft\\Crypto\\RSA
    If one requires to have the full PKCS#12 certificate, the description field
    may be used to locate the corresponding certificate file, located under
    %APPDATA%\\Microsoft\\SystemCertificates\\My\\Certificates
    This description field is encoded in UTF-16LE format at the beginning of the
    certificate file.
    """

    class RSAHeader(probe.DPAPIProbe):
        """This subclass represents the header + modulus, beginning with the
        magic value "RSA1"
        """
        def parse(self, data):
            self.magic = data.eat("4s")  # RSA1
            self.len1 = data.eat("L")
            self.bitlength = data.eat("L")  # 0x400
            self.unk = data.eat("L")  # 0x7F
            self.pubexp = data.eat("L")  # 0x00010001
            self.data = data.eat("%is" % self.len1)
            self.data = self.data[:self.bitlength / 8]  # strip NULL-bytes

        def __repr__(self):
            s = ["RSA header"]
            s.append("\tmagic     = %s" % self.magic)
            s.append("\tbitlength = %d" % self.bitlength)
            s.append("\tunknown   = %x" % self.unk)
            s.append("\tpubexp    = %d" % self.pubexp)
            s.append("\tdata      = %s" % self.data.encode('hex'))
            return "\n".join(s)

    class RSAKey(probe.DPAPIProbe):
        """This subclass represents the RSA privatekey BLOB, beginning with the
        magic value "RSA2"
        """

        class RSAKeyASN1(univ.Sequence):
            """subclass for ASN.1 sequence representing the RSA key pair.
            Mainly useful to export the key to OpenSSL
            """
            componentType = namedtype.NamedTypes(
                namedtype.NamedType('version', univ.Integer()),
                namedtype.NamedType('modulus', univ.Integer()),
                namedtype.NamedType('pubexpo', univ.Integer()),
                namedtype.NamedType('privexpo', univ.Integer()),
                namedtype.NamedType('prime1', univ.Integer()),
                namedtype.NamedType('prime2', univ.Integer()),
                namedtype.NamedType('exponent1', univ.Integer()),
                namedtype.NamedType('exponent2', univ.Integer()),
                namedtype.NamedType('coefficient', univ.Integer())
            )

        def parse(self, data):
            self.magic = data.eat("4s")  # RSA2
            len1 = data.eat("L")
            self.bitlength = data.eat("L")
            chunk = self.bitlength / 16
            self.unk = data.eat("L")
            self.pubexp = data.eat("L")
            self.modulus = data.eat("%is" % len1)[:2 * chunk]
            self.prime1 = data.eat("%is" % (len1 / 2))[:chunk]
            self.prime2 = data.eat("%is" % (len1 / 2))[:chunk]
            self.exponent1 = data.eat("%is" % (len1 / 2))[:chunk]
            self.exponent2 = data.eat("%is" % (len1 / 2))[:chunk]
            self.coefficient = data.eat("%is" % (len1 / 2))[:chunk]
            self.privExponent = data.eat("%is" % len1)[:2 * chunk]
            self.asn1 = self.RSAKeyASN1()
            ll = lambda x: long(x.encode('hex'), 16)
            self.asn1.setComponentByName('version', 0)
            self.asn1.setComponentByName('modulus', ll(self.modulus))
            self.asn1.setComponentByName('pubexpo', self.pubexp)
            self.asn1.setComponentByName('privexpo', ll(self.privExponent))
            self.asn1.setComponentByName('prime1', ll(self.prime1))
            self.asn1.setComponentByName('prime2', ll(self.prime2))
            self.asn1.setComponentByName('exponent1', ll(self.exponent1))
            self.asn1.setComponentByName('exponent2', ll(self.exponent2))
            self.asn1.setComponentByName('coefficient', ll(self.coefficient))

        def __repr__(self):
            s = ["RSA key pair"]
            s.append("\tPublic exponent = %d" % self.pubexp)
            s.append("\tModulus (n)     = %s" % self.modulus.encode('hex'))
            s.append("\tPrime 1 (p)     = %s" % self.prime1.encode('hex'))
            s.append("\tPrime 2 (q)     = %s" % self.prime2.encode('hex'))
            s.append("\tExponent 1      = %s" % self.exponent1.encode('hex'))
            s.append("\tExponent 2      = %s" % self.exponent2.encode('hex'))
            s.append("\tCoefficient     = %s" % self.coefficient.encode('hex'))
            s.append("\tPrivate exponent= %s" % self.privExponent.encode('hex'))
            return "\n".join(s)

        def export(self):
            """This functions exports the RSA key pair in PEM format"""
            import base64
            s = ['-----BEGIN RSA PRIVATE KEY-----']
            text = base64.encodestring(encoder.encode(self.asn1))
            s.append(text.rstrip("\n"))
            s.append('-----END RSA PRIVATE KEY-----')
            return "\n".join(s)

    class RSAPrivKey(probe.DPAPIProbe):
        """Internal use. This represents the DPAPI BLOB containing the RSA
        key pair"""
        def parse(self, data):
            self.dpapiblob = blob.DPAPIBlob(data.remain())

        def postprocess(self, **k):
            self.clearKey = PrivateKeyBlob.RSAKey(self.dpapiblob.cleartext)

        def export(self):
            if self.clearKey is None:
                return ""
            return self.clearKey.export()

        def __repr__(self):
            s = ["RSA Private Key Blob"]
            if self.entropy:
                s.append("entropy = %s" % self.entropy.encode('hex'))
            if hasattr(self, "strong"):
                s.append("strong = %s" % self.strong.encode('hex'))
            if self.dpapiblob.decrypted:
                s.append(repr(self.clearKey))
            s.append(repr(self.dpapiblob))
            return "\n".join(s)

    class RSAFlags(probe.DPAPIProbe):
        """This subclass represents the export flags BLOB"""
        def parse(self, data):
            self.dpapiblob = blob.DPAPIBlob(data.remain())

        def preprocess(self, **k):
            self.entropy = "Hj1diQ6kpUx7VC4m\0"
            if hasattr(k, "strong"):
                self.strong = k["strong"]

        def __repr__(self):
            s = ["Export Flags"]
            s.append("entropy = %s" % self.entropy)
            if hasattr(self, "strong"):
                s.append("strong = %s" % self.strong.encode("hex"))
            s.append("%r" % self.dpapiblob)
            return "\n".join(s)

    def parse(self, data):
        self.version = data.eat("L")
        data.eat("L")  # NULL
        self.descrLen = data.eat("L")
        data.eat("2L")  # NULL NULL
        headerlen = data.eat("L")
        privkeylen = data.eat("L")
        self.crcLen = data.eat("L")
        data.eat("L")  # NULL
        flagslen = data.eat("L")

        self.description = data.eat("%is" % self.descrLen)

        self.header = None
        if headerlen > 0:
            data.eat("5L")  # 20 NULL-bytes ...
            self.header = self.RSAHeader()
            self.header.parse(data.eat_sub(headerlen))

        self.privateKey = None
        if privkeylen > 0:
            self.privateKey = self.RSAPrivKey()
            self.privateKey.parse(data.eat_sub(privkeylen))

        self.flags = None
        if flagslen > 0:
            self.flags = self.RSAFlags()
            self.flags.parse(data.eat_sub(flagslen))

    def try_decrypt_with_hash(self, h, mkp, sid, **k):
        if self.flags != None:
            if self.flags.try_decrypt_with_hash(h, mkp, sid, **k):
                self.privateKey.entropy = self.flags.cleartext
                return self.privateKey.try_decrypt_with_hash(h, mkp, sid, **k)
        else:
            return True
        return False

    def export(self):
        """This functions encodes the RSA key pair in PEM format. Simply calls the same function on the key blob."""
        return self.privateKey.export()

    def __repr__(self):
        s = ["Microsoft Certificate"]
        s.append("\tdescr: %s" % self.description)
        if self.header is not None:
            s.append("+  %r" % self.header)
        if self.privateKey is not None:
            s.append("+  %r" % self.privateKey)
        if self.flags is not None:
            s.append("+  %r" % self.flags)
        return "\n".join(s)


# vim:ts=4:expandtab:sw=4
