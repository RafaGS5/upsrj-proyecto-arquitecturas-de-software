# ============================================================
# Politécnica de Santa Rosa
#
# Materia: Arquitecturas de Software
# Grupo: ISW28
# Archivo: main.py
# Descripción: Este código implementa la estructura base de una aplicación web utilizando el framework Flask en Python.
# Su función principal es crear, configurar y ejecutar una instancia del servidor Flask, siguiendo una arquitectura modular y limpia que separa claramente las responsabilidades del sistema: configuración, definición de rutas y ejecución.
# ============================================================
from flask import Flask
from src.app.routes import register_routes
from src.common.vars import Hosts


def create_app() -> Flask:
    """
    Create and configure the main Flask application.

    Returns:
        Flask: The configured Flask application instance.
    """
    app = Flask(__name__)
    register_routes(app)
    return app

app = create_app()

if __name__ == '__main__':
    app.run(host=Hosts.main[0], port=Hosts.main[1])