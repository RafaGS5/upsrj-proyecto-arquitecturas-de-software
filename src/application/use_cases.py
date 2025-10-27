from datetime import datetime
from uuid import uuid4
from src.domain.models import BinaryFile

class UploadBinaryUseCase:
    def _init_(self, file_repo, db_repo):
        self.file_repo = file_repo
        self.db_repo = db_repo

    def execute(self, file, environment: str) -> BinaryFile:
        binary_id = str(uuid4())
        filename = self.file_repo.save(file, binary_id)
        binary = BinaryFile(
            id = binary_id,
            filename = filename,
            environment = environment,
            status = 'pending' if environment == 'prod' else 'signed',
            uploaded_at = datetime.now()
        )
        self.db_repo.add(binary)
        return binary
    