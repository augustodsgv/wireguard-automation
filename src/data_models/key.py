
from base64 import b64encode, b64decode
from nacl.public import PrivateKey

class Key:
    @classmethod
    def gen_private_key(cls)->str:
        """Generates a new private key"""

        private = PrivateKey.generate()
        return b64encode(bytes(private)).decode("ascii")


    @classmethod
    def gen_public_key(cls, private_key : str)->str:
        """Generates the public key of a private key"""

        private = PrivateKey(b64decode(private_key))
        return b64encode(bytes(private.public_key)).decode("ascii")

    @classmethod
    def is_valid_private_key(cls)->bool:
        """TODO: check if the private key is valid"""
        pass