import base64
import binascii
import ecdsa
import hashlib
import struct
import sys

from Crypto.PublicKey import RSA, DSA

INT_LEN = 4

class InvalidKeyException(Exception):
    pass

class TooShortKeyException(InvalidKeyException):
    pass

class TooLongKeyException(InvalidKeyException):
    pass

class InvalidTypeException(InvalidKeyException):
    pass

class MalformedDataException(InvalidKeyException):
    pass

class SSHKey(object):
    def __init__(self, keydata):
        self.keydata = keydata
        self.current_position = 0
        self.decoded_key = None
        self.rsa = None
        self.dsa = None
        self.ecdsa = None
        self.bits = None
        self.key_type = None
        self.parse()

    def hash(self):
        """ Calculates fingerprint hash.

        Shamelessly copied from http://stackoverflow.com/questions/6682815/deriving-an-ssh-fingerprint-from-a-public-key-in-python

        For specification, see RFC4716, section 4.
        """
        fp_plain = hashlib.md5(self.decoded_key).hexdigest()
        return ':'.join(a+b for a, b in zip(fp_plain[::2], fp_plain[1::2]))

    def unpack_by_int(self):
        """ Returns next data field. """
        # Unpack length of data field
        try:
            requested_data_length = struct.unpack('>I', self.decoded_key[self.current_position:self.current_position+INT_LEN])[0]
        except struct.error:
            raise MalformedDataException("Unable to unpack %s bytes from the data" % INT_LEN)

        # Move pointer to the beginning of the data field
        self.current_position += INT_LEN
        remaining_data_length = len(self.decoded_key[self.current_position:])

        if remaining_data_length < requested_data_length:
            raise MalformedDataException("Requested %s bytes, but only %s bytes available." % (requested_data_length, remaining_data_length))

        next_data = self.decoded_key[self.current_position:self.current_position+requested_data_length]
        # Move pointer to the end of the data field
        self.current_position += requested_data_length
        return next_data

    @classmethod
    def parse_long(cls, data):
        """ Calculate two's complement """
        if sys.version < '3':
            ret = long(0)
            for byte in data:
                ret = (ret << 8) + ord(byte)
        else:
            ret = 0
            for byte in data:
                ret = (ret << 8) + byte
        return ret


    @classmethod
    def split_key(cls, data):
        key_parts = data.strip().split(None, 3)
        if len(key_parts) < 2: # Key type and content are mandatory fields.
            raise InvalidKeyException("Unexpected key format: at least type and base64 encoded value is required")
        return key_parts

    @classmethod
    def decode_key(cls, pubkey_content):
        # Decode base64 coded part.
        try:
            decoded_key = base64.b64decode(pubkey_content.encode("ascii"))
        except (TypeError, binascii.Error):
            raise InvalidKeyException("Unable to decode the key")
        return decoded_key

    def parse(self):
        self.current_position = 0
        key_parts = self.split_key(self.keydata)

        key_type = key_parts[0]
        pubkey_content = key_parts[1]

        self.decoded_key = self.decode_key(pubkey_content)

        # Check key type
        unpacked_key_type = self.unpack_by_int()
        if key_type != unpacked_key_type.decode():
            raise InvalidTypeException("Keytype mismatch: %s != %s" % (key_type, unpacked_key_type))

        self.key_type = unpacked_key_type

        min_length = max_length = None

        if self.key_type == b"ssh-rsa":

            raw_e = self.unpack_by_int()
            raw_n = self.unpack_by_int()

            unpacked_e = self.parse_long(raw_e)
            unpacked_n = self.parse_long(raw_n)

            self.rsa = RSA.construct((unpacked_n, unpacked_e))
            self.bits = self.rsa.size() + 1

            min_length = 768
            max_length = 16384

        elif self.key_type == b"ssh-dss":
            data_fields = {}
            for item in ("p", "q", "g", "y"):
                data_fields[item] = self.parse_long(self.unpack_by_int())

            self.dsa = DSA.construct((data_fields["y"], data_fields["g"], data_fields["p"], data_fields["q"]))
            self.bits = self.dsa.size() + 1

            min_length = max_length = 1024

        elif self.key_type.strip().startswith(b"ecdsa-sha"):
            curve_information = self.unpack_by_int()
            curve_data = {b"nistp256": (ecdsa.curves.NIST256p, hashlib.sha256),
                          b"nistp192": (ecdsa.curves.NIST192p, hashlib.sha256),
                          b"nistp224": (ecdsa.curves.NIST224p, hashlib.sha256),
                          b"nistp384": (ecdsa.curves.NIST384p, hashlib.sha384),
                          b"nistp521": (ecdsa.curves.NIST521p, hashlib.sha512)}
            if curve_information not in curve_data:
                raise NotImplementedError("Invalid curve type: %s" % curve_information)
            curve, hash_algorithm = curve_data[curve_information]

            data = self.unpack_by_int()

            ecdsa_key = ecdsa.VerifyingKey.from_string(data[1:], curve, hash_algorithm)
            self.bits = int(curve_information.replace(b"nistp", b"")) # TODO
            self.ecdsa = ecdsa_key
        elif self.key_type == b"ssh-ed25519":
            # There is no (apparent) way to validate ed25519 keys. This only
            # checks data length (256 bits), but does not try to validate
            # the key in any way.
            verifying_key = self.unpack_by_int()
            verifying_key_length = len(verifying_key) * 8

            min_length = max_length = 256
            self.bits = verifying_key_length
        else:
            raise NotImplementedError("Invalid key type: %s" % self.key_type)

        if min_length:
            if self.bits < min_length:
                raise TooShortKeyException("%s key data can not be shorter than %s bits (was %s)" % (self.key_type, min_length, self.bits))
        if max_length:
            if self.bits > max_length:
                raise TooLongKeyException("%s key data can not be longer than %s bits (was %s)" % (self.key_type, min_length, self.bits))

        if self.current_position != len(self.decoded_key):
            raise MalformedDataException("Leftover data: %s bytes" % (len(self.decoded_key) - self.current_position))
