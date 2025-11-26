from datetime import datetime
from uuid import uuid4
from typing import List, Dict, Any, Optional

from src.domain.models import BinaryFile
from src.infrastructure.json_repository import JsonRepository
from src.infrastructure.file_repository import FileRepository
from src.domain.services import SigningService


class UploadBinaryUseCase:
    """
    Caso de uso para subir un binario.
    Si environment == 'prod' y hay email_service + user_email,
    se dispara el envío de correo de aprobación.
    """

    def __init__(
        self,
        file_repo: FileRepository,
        json_repo: JsonRepository,
        email_service=None,
    ):
        self.file_repo = file_repo
        self.json_repo = json_repo
        self.email_service = email_service

    def execute(
        self,
        file,
        environment: str,
        user_email: Optional[str] = None,
    ) -> BinaryFile:
        print(f"[UploadBinaryUseCase] Ejecutando upload. environment={environment}, user_email={user_email}")

        binary_id = str(uuid4())
        filename = self.file_repo.save(file, binary_id)

        binary = BinaryFile(
            file_id=binary_id,
            filename=filename,
            environment=environment,
            status="pending",
            uploaded_at=datetime.now().isoformat(),
        )

        # Guardar en "BD" (JSON)
        self.json_repo.add_record(binary.to_dict())
        print(f"[UploadBinaryUseCase] Archivo guardado con id={binary.id}, filename={binary.filename}")

        # Lógica de producción: enviar correo
        if environment == "prod":
            print("[UploadBinaryUseCase] Entorno prod detectado.")
        else:
            print("[UploadBinaryUseCase] Entorno dev, NO se enviará correo.")

        if environment == "prod" and self.email_service and user_email:
            from src.infrastructure.email_service import EmailService  # evita problemas de import circular
            print("[UploadBinaryUseCase] Intentando enviar correo de aprobación...")
            ok = self.email_service.send_approval_email(
                user_email,
                binary.id,
                binary.filename,
            )
            print(f"[UploadBinaryUseCase] Resultado envío correo: {ok}")
        else:
            if environment == "prod" and not user_email:
                print("[UploadBinaryUseCase] environment=prod pero user_email es None.")
            if environment == "prod" and not self.email_service:
                print("[UploadBinaryUseCase] environment=prod pero no hay email_service.")

        return binary


class ListFilesUseCase:
    """
    Devuelve la lista de registros almacenados.
    Lo dejamos en dicts para que Flask pueda hacer jsonify() sin problemas.
    """

    def __init__(self, db_repo: JsonRepository):
        self.db_repo = db_repo

    def execute(self) -> List[Dict[str, Any]]:
        try:
            records = self.db_repo.list_records()
            # Aseguramos que sean dicts, no objetos BinaryFile
            normalized: List[Dict[str, Any]] = []
            for r in records:
                if isinstance(r, BinaryFile):
                    normalized.append(r.to_dict())
                else:
                    normalized.append(r)
            return normalized
        except Exception as e:
            print(f"[ListFilesUseCase] Error retrieving records: {e}")
            return []


class SignBinaryUseCase:
    """
    Firma un archivo y actualiza su registro en el JSON.
    """

    def __init__(
        self,
        file_repo: FileRepository,
        json_repo: JsonRepository,
        signing_service: SigningService,
    ):
        self.file_repo = file_repo
        self.json_repo = json_repo
        self.signing_service = signing_service

    def execute(self, file_id: str) -> Optional[BinaryFile]:
        record = self.json_repo.get_record(file_id)

        if record is None:
            print(f"[SignBinaryUseCase] Record not found for file id: {file_id}")
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
                    "signature": binary.signature,
                },
            )

            print(f"[SignBinaryUseCase] File '{binary.filename}' signed successfully.")
            return binary

        except Exception as e:
            print(f"[SignBinaryUseCase] Error while signing file '{file_id}': {e}")
            return None


class ApproveBinaryUseCase:
    """
    Caso de uso que se ejecuta cuando se abre el enlace del correo.
    """

    def __init__(self, sign_use_case: SignBinaryUseCase):
        self.sign_use_case = sign_use_case

    def execute(self, file_id: str) -> bool:
        result = self.sign_use_case.execute(file_id)
        return result is not None
