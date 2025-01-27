import os
base_dir = os.path.abspath(os.path.dirname(__file__)) # указываем путь к папке проекта(abspath - точная (абсолютная) дорога (путь к папке))
class Config:
    TURSO_AUTH_TOKEN = os.environ.get("TURSO_AUTH_TOKEN")
    TURSO_DATABASE_URL = os.environ.get("TURSO_DATABASE_URL")
    SQLALCHEMY_DATABASE_URI = f"sqlite+{TURSO_DATABASE_URL}/?authToken{TURSO_AUTH_TOKEN}&secure=true" # адрес базы данных (ключ к базе данных)