from Crypto.Hash import SHA256
from Crypto.Signature import PKCS1_v1_5
from Crypto.PublicKey import RSA
import base64


def generate_keys():
    private_key = RSA.generate(1024)
    public_key = private_key.publickey()

    return public_key, private_key


def sign(message, private_key):
    digest = SHA256.new()
    digest.update(message)
    signer = PKCS1_v1_5.new(private_key)
    sig = signer.sign(digest)

    return sig


def load_key(key):
    key = base64.b64decode(key)
    return RSA.importKey(key)


def serialize_key(key):
    key = key.exportKey("PEM")
    return base64.b64encode(key)


def verify(message, key, sig):
    digest = SHA256.new()
    digest.update(message)
    verifier = PKCS1_v1_5.new(key)
    verified = verifier.verify(digest, sig)

    return verified
