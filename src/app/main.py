# ============================================================
# Punto de entrada de la app Flask (interfaz web)
# ============================================================
import sys
from pathlib import Path


sys.path.append(str(Path(__file__).parent.parent.parent))

from flask import Flask
from flask_mail import Mail

from src.app.routes import register_routes
from src.common.vars import HOME_HOST


def create_app() -> Flask:
    app = Flask(__name__, template_folder="templates")


    app.config["MAIL_SERVER"] = "smtp.gmail.com"
    app.config["MAIL_PORT"] = 587
    app.config["MAIL_USE_TLS"] = True


    app.config["MAIL_USERNAME"] = "rafa2005w@gmail.com"
    app.config["MAIL_PASSWORD"] = "xtkn hpwd nwlf kada"


    app.config["MAIL_DEFAULT_SENDER"] = app.config["MAIL_USERNAME"]


    app.config["MAIL_RECIPIENT"] = "023000741@upsrj.edu.mx"

    app.mail = Mail(app)
    register_routes(app)
    return app


app = create_app()

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=HOME_HOST, debug=True)
