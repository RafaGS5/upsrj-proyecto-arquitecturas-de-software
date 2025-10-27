from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.primitives.asymmetric import padding

class SigningService:
    def __init__(self, key_loader):
        self.keyloader = key_loader

    def sign_binary(self, binary_data: bytes, private_key_path: str) -> bytes:
        private_key = self.key_loader(private_key_path)
        return private_key.sign(
        binary_data,
        padding.PKCS1v15(),
        hashes.SHA256()
    )    