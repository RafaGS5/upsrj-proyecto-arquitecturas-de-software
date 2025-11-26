# ============================================================
# Servicios de dominio: lógica pura (firma de binarios)
# ============================================================
import os
import hashlib
from typing import Tuple

from src.domain.models import BinaryFile
from src.common.vars import DATA_DIR, SIGNED_DIR


class SigningService:
    def __init__(self, output_dir: str = SIGNED_DIR):
        self.output_dir = output_dir

    def sign_file(self, binary: BinaryFile) -> Tuple[str, str]:
        """
        Firma un archivo binario calculando SHA-256 y generando una copia firmada.

        Returns:
            (signature_hex, signed_path)
        """
        try:
      
            filename_only = os.path.basename(binary.filename)

         
            source_path = os.path.join(DATA_DIR, filename_only)

     
            signed_filename = f"signed_{filename_only}"
            signed_path = os.path.join(self.output_dir, signed_filename)

       
            sha256_hash = hashlib.sha256()
            with open(source_path, "rb") as file:
                for block in iter(lambda: file.read(4096), b""):
                    sha256_hash.update(block)

            signature = sha256_hash.hexdigest()

            with open(source_path, "rb") as src, open(signed_path, "wb") as dst:
                dst.write(src.read())
                dst.write(b"\n\n# SIGNATURE: " + signature.encode("utf-8"))

            print(f"[SigningService] File '{filename_only}' signed successfully.")
            return signature, signed_path

        except Exception as e:
            print(f"[SigningService] Error while signing '{binary.filename}': {e}")
            raise
