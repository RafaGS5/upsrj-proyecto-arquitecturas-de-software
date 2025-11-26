# ============================================================
# Universidad Politécnica de Santa Rosa Jáuregui
#
# Materia: Arquitecturas de Software
# Profesor: Jesús Salvador López Ortega
# Alumno: Rafael Guerrero Sanchez
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
    SignBinaryUseCase,
    ApproveBinaryUseCase,
    ListFilesUseCase,
)
from src.infrastructure.file_repository import FileRepository
from src.infrastructure.json_repository import JsonRepository
from src.infrastructure.email_service import EmailService
from src.domain.services import SigningService
from src.domain.models import BinaryFile


def register_routes(app):

    @app.route("/")
    def home():
        return render_template("home.html")


    @app.route("/files", methods=["GET"])
    def list_files():
        use_case = ListFilesUseCase(JsonRepository())
        records = use_case.execute()


        normalized = []
        for r in records:
            if isinstance(r, BinaryFile):
                normalized.append(r.to_dict())
            else:
                normalized.append(r)

        return jsonify(normalized), 200

    @app.route("/upload", methods=["POST"])
    def upload_binary():
        file = request.files["file"]
        environment = request.form.get("environment", "dev")

        print(f"[routes] /upload recibido. environment={environment}")

        target_email = app.config.get("MAIL_RECIPIENT") or app.config.get("MAIL_USERNAME")
        print(f"[routes] MAIL_RECIPIENT(or USERNAME)={target_email}")

        use_case = UploadBinaryUseCase(
            FileRepository(),
            JsonRepository(),
            EmailService(),
        )

        binary = use_case.execute(file, environment, target_email)
        return jsonify(binary.to_dict()), 200
    @app.route("/sign", methods=["POST"])
    def sign_file():
        data = request.get_json(force=True)
        file_id = data.get("file_id")

        use_case = SignBinaryUseCase(
            FileRepository(),
            JsonRepository(),
            SigningService(),
        )
        result = use_case.execute(file_id)

        if result:
            return jsonify(result.to_dict()), 200
        return jsonify({"error": "Error signing"}), 500


    @app.route("/approve/<file_id>", methods=["GET"])
    def approve_file(file_id: str):
        sign_use_case = SignBinaryUseCase(
            FileRepository(),
            JsonRepository(),
            SigningService(),
        )
        approve_use_case = ApproveBinaryUseCase(sign_use_case)

        ok = approve_use_case.execute(file_id)
        if ok:
            return """
            <div style="font-family: sans-serif; text-align: center; padding: 50px;">
                <h1 style="color: #28a745;">Archivo aprobado y firmado</h1>
                <p>El proceso de producción ha finalizado correctamente.</p>
                <p>Puede cerrar esta ventana.</p>
            </div>
            """
        else:
            return (
                "<h1 style='color: red;'>Error</h1>"
                "<p>El archivo no existe o ya fue firmado.</p>"
            )


    @app.route("/clear", methods=["POST"])
    def clear_history():
        try:
            JsonRepository().delete_all()
            FileRepository().delete_all()
            return jsonify({"msg": "ok"}), 200
        except Exception:
            return jsonify({"error": "err"}), 500
