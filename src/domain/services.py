from src.domain.models import BinaryFile
from typing import Tuple
from src.common.vars import DATA_DIR, SIGNED_DIR
import os
import hashlib

class SigningService:
    
    def __init__(self, output_dir: str = SIGNED_DIR):
        self.output_dir = output_dir
    
    def sign_file(self, binary: BinaryFile) -> Tuple[str, str]:
        try:
            source_path = os.path.join(DATA_DIR, binary.filename)
            signed_path = os.path.join(self.output_dir)
        
            # Compute SHA-256 signature
            sha256_hash = hashlib.sha256()
            with open(source_path, 'rb') as file:
                for block in iter(lambda: file.read(4096), b""):
                    sha256_hash.update(block)
            signature = sha256_hash.hexdigest()
            
            # Create signed copy
            with open(source_path, 'rb') as src, open(signed_path, 'wb') as dst:
                dst.write(src.read())
                dst.write(b"\n\n# SIGNATURE: " + signature.encode("utf-8"))
            
            print(f"[SigningService] File '{binary.filename}' signed successfully.")            
            return signature, signed_path
        
        except Exception as e:
            print(f"[SigningService] Error while signing '{binary.filename}':{e}")
            raise