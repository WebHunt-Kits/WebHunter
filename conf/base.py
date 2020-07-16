import os

SERVICE_NAME = "webhunter"
DOMAIN = os.getenv("DOMAIN", default="hunter.imipy.com")
ALLOW_METHODS = ("GET", "POST", "PUT", "DELETE", "OPTIONS")

BASE_DIR = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))
LOG_DIR = os.path.join(BASE_DIR, "logs")

MIDDLEWARES = [
    "core.middlewares.Cors",
    "flask_mico.middleware.Translate",
    "core.middlewares.Authentication",
    "core.middlewares.VerifyApiSign"
]

EXTENSIONS = [
    "core.extensions.db"
]

COMMANDS = [
    "core.commands.init_db"
]

ROOT_URLCONF = "webhunter.urls"
