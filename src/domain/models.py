# Alumno: Rfael Guerrero Sanchez
from datetime import datetime

class BinaryFile(object):
    """
    Entidad de dominio que representa un archivo binario.
    """

    def __init__(
        self,
        file_id: str,
        filename: str,
        environment: str,
        status: str,
        uploaded_at: str | None = None,
        signed_path: str | None = None,
        signature: str | None = None
    ) -> None:
        self.id = file_id
        self.filename = filename          # ruta completa del archivo en disco
        self.environment = environment    # 'dev' o 'prod'
        self.status = status              # 'pending', 'approved', 'signed', etc.
        self.uploaded_at = uploaded_at or datetime.now().isoformat()
        self.signed_path = signed_path
        self.signature = signature

    def to_dict(self) -> dict:
        """Convierte la entidad a un diccionario serializable."""
        return {
            "id": self.id,
            "filename": self.filename,
            "environment": self.environment,
            "status": self.status,
            "uploaded_at": self.uploaded_at,
            "signed_path": self.signed_path,
            "signature": self.signature,
        }

    @classmethod
    def from_dict(cls, data: dict) -> "BinaryFile":
        """Crea una instancia de BinaryFile desde un diccionario."""
        return cls(
            file_id=data.get("id"),
            filename=data.get("filename"),
            environment=data.get("environment"),
            status=data.get("status"),
            uploaded_at=data.get("uploaded_at"),
            signed_path=data.get("signed_path"),
            signature=data.get("signature"),
        )