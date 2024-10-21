from app import app, db
import sqlalchemy as alchemy
import sqlalchemy.orm as orm
from app.models import User, Post

@app.shell_context_processor # функция для подачи данных в терминал(сервер)
def make_shell_context():
    return {"alchemy":alchemy, "db":db, "orm":orm, "User":User, "Post":Post}
