import os

# Ruta base del proyecto (carpeta raíz que contiene "src", "data", etc.)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Directorios principales
ROOT_DIR = BASE_DIR
SRC_DIR = os.path.join(ROOT_DIR, "src")

# Aquí se guardan los binarios subidos y los firmados
DATA_DIR = os.path.join(ROOT_DIR, "data", "binaries")
SIGNED_DIR = os.path.join(ROOT_DIR, "data", "signed")

# Carpeta de templates de Flask
TEMPLATES_DIR = os.path.join(SRC_DIR, "app", "templates")

# Puerto donde se levanta la app web
HOME_HOST = 8080

# Crear carpetas de almacenamiento
os.makedirs(DATA_DIR, exist_ok=True)
os.makedirs(SIGNED_DIR, exist_ok=True)
