import os
base_dir = os.path.abspath(os.path.dirname(__file__)) # указываем путь к папке проекта(abspath - точная (абсолютная) дорога (путь к папке))
class Config:
    SECRET_KEY = os.environ.get("SECRET_KEY") or "Alex" # временный ключ - Alex
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or "sqlite:///" + os.path.join(base_dir, "app.db") # адрес базы данных (ключ к базе данных)