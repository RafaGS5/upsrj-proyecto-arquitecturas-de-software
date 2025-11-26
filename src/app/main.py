# ============================================================
# Punto de entrada de la app Flask (interfaz web)
# ============================================================
import sys
from pathlib import Path

# Ajuste de rutas para poder hacer imports tipo "from src..."
sys.path.append(str(Path(__file__).parent.parent.parent))

from flask import Flask
from flask_mail import Mail

from src.app.routes import register_routes
from src.common.vars import HOME_HOST


def create_app() -> Flask:
    app = Flask(__name__, template_folder="templates")

    # --- CONFIGURACIÓN DEL CORREO (como en el proyecto 2 del profe) ---
    app.config["MAIL_SERVER"] = "smtp.gmail.com"
    app.config["MAIL_PORT"] = 587
    app.config["MAIL_USE_TLS"] = True

    # ⚠️ Demo: credenciales usadas en el proyecto 2
    # En un proyecto real, usa variables de entorno
    app.config["MAIL_USERNAME"] = "proyecto3287@gmail.com"
    app.config["MAIL_PASSWORD"] = "gkxy knmh fuav xdex"

    app.config["MAIL_DEFAULT_SENDER"] = app.config["MAIL_USERNAME"]

    # Inicializar Flask-Mail y colgarlo en app
    app.mail = Mail(app)

    # Registrar rutas
    register_routes(app)
    return app


app = create_app()

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=HOME_HOST, debug=True)
