import os

# Base directory of the project
BASE_DIR = os.path.abspath(os.path.dirname(__file__))

class Config:
    # Secret key for sessions
    SECRET_KEY = "inventory_secret_key"

    # SQLite Database
    SQLALCHEMY_DATABASE_URI = "sqlite:///" + os.path.join(BASE_DIR, "inventory.db")
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # Folder for uploaded product images
    UPLOAD_FOLDER = os.path.join(BASE_DIR, "static", "uploads")

    # Maximum upload size (16 MB)
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024

    # Allowed image file extensions
    ALLOWED_EXTENSIONS = {"png", "jpg", "jpeg", "gif", "webp"}