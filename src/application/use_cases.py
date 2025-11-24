from datetime import datetime
from uuid import uuid4
from src.domain.models import BinaryFile
from typing import List, Dict, Any, Optional
from src.infrastructure.json_repository import JsonRepository
from src.infrastructure.file_repository import FileRepository
from src.domain.services import SigningService


class UploadBinaryUseCase:
    
    def __init__(self, file_repo:FileRepository, json_repo: JsonRepository):
        self.file_repo = file_repo
        self.json_repo = json_repo
    
    def execute(self, file, environment: str) -> BinaryFile:
        binary_id = str(uuid4())
        filename = self.file_repo.save(file, binary_id)
        binary = BinaryFile(
            file_id = binary_id,
            filename = filename,
            environment = environment,
            status = 'pending' if environment == 'prod' else 'signed',
            uploaded_at = datetime.now()
        )
        self.json_repo.add_record(binary)
        return binary
    
class ListFilesUseCase:
    def __init__(self, db_repo: JsonRepository):
        self.db_repo = db_repo

    def execute(self) -> List[Dict[str, Any]]:
        try:
            records = self.db_repo.list_records()
            return records
        except Exception as e:
            print(f"[ListFilesUseCase] Error retrieving records: {e}")
            return []
        
class SignBinaryUseCase:
    
    def __init__(self, file_repo: FileRepository, json_repo: JsonRepository, signing_service: SigningService):
        self.file_repo = file_repo
        self.json_repo = json_repo
        self.signing_service = signing_service
            
    def execute(self, file_id: str) -> Optional[BinaryFile]:
        record = self.json_repo.get_record(file_id)
        
        if record is None:
            print(f"[SignBinaryUseCase] Record not found for file id:", file_id)
            return None
        
        try:
            binary = BinaryFile.from_dict(record)
            signature, signed_path = self.signing_service.sign_file(binary)

            binary.status = "signed"
            binary.signed_path = signed_path
            binary.signature = signature
            
            self.json_repo.update_record(
                binary.id,
                {
                    "status": binary.status,
                    "signed_path": binary.signed_path,
                    "signature": binary.signature
                }
            )
            
            print(f"[SignBinaryUseCase] File '{binary.filename}' signed successfully.")
            return binary
        
        except Exception as e:
            print(f"[SignBinaryUseCase] Error while signing file '{file_id}': {e}")
            return None
            