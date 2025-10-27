from flask import Flask
from src.app.routes import register_routes
from vars import host

def create_app():
    app = Flask(__name__)
    register_routes(app)
    return app

app = create_app()

if __name__ == '__main__':
    app.run(host=Hosts.main[0], port=Host.main[1])

