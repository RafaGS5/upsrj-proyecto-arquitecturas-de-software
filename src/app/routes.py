# ============================================================
# Universidad Politécnica de Santa Rosa Jáuregui
#
# Materia: Arquitecturas de Software
# Profesor: Jesús Salvador López Ortega
# Grupo: ISW28
# Archivo: routes.py
# Descripción: Define la ruta /upload para recibir archivos mediante 
# solicitudes POST. Usa el caso de uso UploadBinaryUseCase junto con 
# los repositorios FileRepository y JsonRepository para procesar y 
# almacenar los archivos binarios según el entorno especificado.
# ============================================================

from flask import request, jsonify, render_template
from src.application.use_cases import UploadBinaryUseCase
from src.infrastructure.file_repository import FileRepository
from src.infrastructure.json_repository import JsonRepository

def register_routes(app):
    """
    Register HTTP routes for the Flask application.

    This function attaches all routes related to file uploads to the given
    Flask application instance. It defines an endpoint that handles binary
    file uploads and delegates the logic to the UploadBinaryUseCase class.

    Args:
        app (Flask): The Flask application instance used to register routes.

    Routes:
        /upload (POST): 
            Receives a file and an optional environment variable. 
            Executes the upload use case to process the binary file and 
            returns the file ID and its upload status in JSON format.
    """
    @app.route("/")
    def home():
        return render_template("home.html")
    

    @app.route("/upload", methods=["POST"])
    def upload_file():
        """
        Handle the file upload request.

        This endpoint retrieves a binary file and an optional environment
        parameter from the incoming POST request. It initializes the 
        UploadBinaryUseCase with the appropriate repositories, executes 
        the upload operation, and returns the resulting file information.

        Returns:
            Response: A JSON object containing:
                - id (str): The identifier of the uploaded binary file.
                - status (str): The current status of the uploaded file.
        """
        # Retrieve file input and environment variable 
        file = request.files['file']
        environment = request.form.get('environment', 'dev')

        
        # Invoque "upload binary use case" with current context
        use_case = UploadBinaryUseCase(FileRepository(), JsonRepository())
        binary = use_case.execute(file, environment)

        # Return response as JSON
        return jsonify({'id': binary.id, 'status': binary.status})
        