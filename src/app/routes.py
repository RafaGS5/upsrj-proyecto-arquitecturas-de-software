# ============================================================
# Universidad Politécnica de Santa Rosa Jáuregui
#
# Materia: Arquitecturas de Software
# Profesor: Jesús Salvador López Ortega
# Grupo: ISW28
# Archivo: routes.py
# Descripción:
#   Define las rutas principales de la app de firmado binario:
#   - GET  /       -> renderiza la vista principal (home.html)
#   - POST /upload -> sube un archivo binario y lo registra
#   - POST /sign   -> firma un archivo (dev) o difiere la firma (prod)
#   - GET  /files  -> lista todos los binarios registrados en JSON
# ============================================================

from flask import request, jsonify, render_template

from src.application.use_cases import (
    UploadBinaryUseCase,
    ListFilesUseCase,
    SignBinaryUseCase,
)
from src.infrastructure.file_repository import FileRepository
from src.infrastructure.json_repository import JsonRepository
from src.domain.services import SigningService
from src.domain.models import BinaryFile


def register_routes(app):

    # ---------- Vista principal ----------
    @app.route("/", methods=["GET"])
    def home():
        return render_template("home.html")

    # ---------- Subir archivo ----------
    @app.route("/upload", methods=["POST"])
    def upload_binary():
        """
        Recibe un archivo binario y el entorno (dev/prod).
        Usa UploadBinaryUseCase para guardar el archivo y registrar metadatos.
        """
        file = request.files.get("file")
        environment = request.form.get("environment", "dev")

        if not file:
            return jsonify({"error": "No file provided"}), 400

        try:
            use_case = UploadBinaryUseCase(
                file_repo=FileRepository(),
                json_repo=JsonRepository(),
            )
            binary = use_case.execute(file, environment)

            return jsonify(binary.to_dict()), 200

        except Exception as e:
            print(f"[Route /upload] ERROR: {e}")
            return jsonify({"error": str(e)}), 500

    # ---------- Firmar archivo ----------
    @app.route("/sign", methods=["POST"])
    def sign_file():
        """
        Firma un archivo por ID. Para 'prod' solo difiere la firma;
        para 'dev' realiza la firma inmediatamente.
        """
        try:
            data = request.get_json() or {}
            file_id = data.get("file_id")

            if not file_id:
                return jsonify({"error": "Missing file_id in request body"}), 400

            json_repo = JsonRepository()
            file_repo = FileRepository()
            signing_service = SigningService()

            use_case = SignBinaryUseCase(
                file_repo=file_repo,
                json_repo=json_repo,
                signing_service=signing_service,
            )

            # Recuperar el registro para ver el entorno
            record = json_repo.get_record(file_id)
            if record is None:
                return jsonify({"error": "File not found"}), 404

            binary = record if isinstance(record, BinaryFile) else BinaryFile.from_dict(record)

            # Si es prod, NO firmamos todavía
            if binary.environment == "prod":
                return jsonify(
                    {
                        "id": binary.id,
                        "filename": binary.filename,
                        "environment": binary.environment,
                        "status": binary.status,
                        "message": "Signing deferred for production. Manual approval required.",
                    }
                ), 200

            # Si es dev, firmamos
            signed_binary = use_case.execute(file_id=file_id)
            if signed_binary is None:
                return jsonify({"error": "Signing failed"}), 500

            return jsonify(signed_binary.to_dict()), 200

        except Exception as e:
            print(f"[Route /sign] ERROR: {e}")
            return jsonify({"error": str(e)}), 500

    # ---------- Listar archivos ----------
    @app.route("/files", methods=["GET"])
    def list_files():
        """
        Devuelve un ARREGLO JSON con todos los BinaryFile.
        Convierte cada BinaryFile a dict antes de pasarlo a jsonify.
        """
        try:
            json_repo = JsonRepository()
            use_case = ListFilesUseCase(json_repo=json_repo)

            binaries = use_case.execute()  # -> List[BinaryFile]

            # 🔹 AQUÍ está la magia: convertir objetos a dict
            payload = [b.to_dict() for b in binaries]

            print(f"[Route /files] returning {len(payload)} records")
            return jsonify(payload), 200

        except Exception as e:
            print(f"[Route /files] ERROR: {e}")
            return jsonify({"error": str(e)}), 500