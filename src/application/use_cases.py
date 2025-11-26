from datetime import datetime
from uuid import uuid4
from typing import List, Optional

from src.domain.models import BinaryFile
from src.infrastructure.json_repository import JsonRepository
from src.infrastructure.file_repository import FileRepository
from src.domain.services import SigningService


class UploadBinaryUseCase:
    """
    Caso de uso para subir un archivo binario.
    """

    def __init__(self, file_repo: FileRepository, json_repo: JsonRepository) -> None:
        self.file_repo = file_repo
        self.json_repo = json_repo

    def execute(self, file, environment: str) -> BinaryFile:
        if environment not in ("dev", "prod"):
            raise ValueError("Invalid environment. Must be 'dev' or 'prod'.")

        file_id = str(uuid4())

        # Guardar archivo físico original
        stored_path = self.file_repo.save(file, file_id=file_id, signed=False)

        # Crear entidad de dominio
        binary = BinaryFile(
            file_id=file_id,
            filename=stored_path,  # ruta completa en disco
            environment=environment,
            status="pending",
            uploaded_at=datetime.now().isoformat(),
            signed_path=None,
            signature=None,
        )

        # Guardar metadatos en JSON
        self.json_repo.add_record(binary.to_dict())

        return binary


class ListFilesUseCase:
    """
    Caso de uso para listar todos los registros.
    """

    def __init__(self, json_repo: JsonRepository) -> None:
        self.json_repo = json_repo

    def execute(self) -> List[BinaryFile]:
        records = self.json_repo.list_records()
        return [BinaryFile.from_dict(r) for r in records]


class ApproveBinaryUseCase:
    """
    Marca un archivo como 'approved' (por si lo usas para PROD).
    """

    def __init__(self, json_repo: JsonRepository) -> None:
        self.json_repo = json_repo

    def execute(self, file_id: str) -> Optional[BinaryFile]:
        record = self.json_repo.get_record(file_id)
        if record is None:
            return None

        binary = BinaryFile.from_dict(record)
        binary.status = "approved"
        self.json_repo.update_record(binary.id, {"status": binary.status})
        return binary


class SignBinaryUseCase:
    """
    Caso de uso para firmar un archivo binario.

    IMPORTANTE:
    - El SigningService YA escribe el archivo firmado en disco
      y devuelve la ruta de ese archivo.
    - Aquí solo actualizamos el registro en JSON.
    """

    def __init__(
        self,
        file_repo: FileRepository,          # ahora mismo no lo usamos, pero lo dejamos para no romper imports
        json_repo: JsonRepository,
        signing_service: SigningService,
    ) -> None:
        self.file_repo = file_repo
        self.json_repo = json_repo
        self.signing_service = signing_service

    def execute(self, file_id: str) -> Optional[BinaryFile]:
        record = self.json_repo.get_record(file_id)

        if record is None:
            print(f"[SignBinaryUseCase] Record not found for file id: {file_id}")
            return None

        try:
            # Aseguramos una instancia de BinaryFile
            binary = record if isinstance(record, BinaryFile) else BinaryFile.from_dict(record)

            # Firmar el archivo -> ahora devuelve (firma, ruta_archivo_firmado)
            signature, signed_path = self.signing_service.sign_file(binary)

            # Actualizar entidad
            binary.status = "signed"
            binary.signature = signature
            binary.signed_path = signed_path

            # Persistir cambios en la "BD" JSON
            self.json_repo.update_record(
                binary.id,
                {
                    "status": binary.status,
                    "signed_path": binary.signed_path,
                    "signature": binary.signature,
                },
            )

            print(f"[SignBinaryUseCase] File '{binary.filename}' signed and saved successfully.")
            return binary

        except Exception as e:
            print(f"[SignBinaryUseCase] Error while signing file '{file_id}': {e}")
            return None
