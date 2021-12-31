from Crypto.Hash import SHA256
from Crypto.Signature import PKCS1_v1_5
from Crypto.PublicKey import RSA
import base64


def generate_keys():
    private_key = RSA.generate(1024)
    public_key = private_key.publickey()

    return public_key, private_key


def encrypt(message, key):
    return key.encrypt(message)


def decrypt(message, key):
    return key.decrypt(message)


def load_key(key):
    key = base64.b64decode(key)
    return RSA.importKey(key)


def serialize_key(key):
    key = base64.b64encode(key.exportKey("DER")).decode("utf-8")
    return key


def sign(message, private_key):
    digest = SHA256.new()
    digest.update(str(message).encode("utf-8"))
    signer = PKCS1_v1_5.new(private_key)
    sig = signer.sign(digest)

    return base64.b64encode(sig).decode("utf-8")


def verify(message, sig, key):
    digest = SHA256.new()
    digest.update(str(message).encode("utf-8"))
    verifier = PKCS1_v1_5.new(key)
    verified = verifier.verify(digest, base64.b64decode(sig))

    return verified
