
import os
import shutil
from datetime import datetime
from typing import BinaryIO

import os
import shutil
from datetime import datetime
from typing import BinaryIO

class FileRepository(object):
    
    def __init__(self, base_path: str = "data"):
        self.binary_dir = "data/binaries"
        self.signed_dir = "data/signed"
        self.__ensure_directories()

    def __ensure_directories(self) -> None:
        for directory in [self.binary_dir, self.signed_dir]:
            if not os.path.exists(directory):
                os.makedirs(directory)

    def save(self, file: BinaryIO, file_id: str, signed: bool = False) -> str:
        directory = self.signed_dir if signed else self.binary_dir
        filename = f"{file_id}{datetime.now().strftime('%Y%m%d%H%M%S')}.bin"
        file_path = os.path.join(directory, filename)

        if hasattr(file, "save"):  # Flask FileStorage
            file.save(file_path)
        else:
            with open(file_path, "wb") as f:
                f.write(file.read() if hasattr(file, "read") else file)

        return file_path

    def load(self, file_path: str) -> bytes:
        
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"File not found: {file_path}")

        with open(file_path, "rb") as f:
            return f.read()

    def delete(self, file_path: str) -> None:
        
        if os.path.exists(file_path):
            os.remove(file_path)
            
    def move_to_signed(self, original_path: str, signed_data: bytes) -> str:
        
        filename = os.path.basename(original_path)
        signed_path = os.path.join(self.signed_dir, f"signed_{filename}")

        with open(signed_path, "wb") as signed_file:
            signed_file.write(signed_data)

        return signed_path

    def list_files(self, signed: bool = False) -> list:
        directory = self.signed_dir if signed else self.binary_dir
        return sorted(os.listdir(directory))