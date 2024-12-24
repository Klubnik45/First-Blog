from werkzeug.security import generate_password_hash, check_password_hash
from typing import Optional
import sqlalchemy as alchemy
import sqlalchemy.orm as orm
from app import db, login
from datetime import datetime, timezone
from flask_login import UserMixin
from hashlib import md5

class User(db.Model, UserMixin):
    id: orm.Mapped[int] = orm.mapped_column(primary_key=True)
    username: orm.Mapped[str] = orm.mapped_column(alchemy.String(64), index=True, unique=True)
    email: orm.Mapped[str] = orm.mapped_column(alchemy.String(120), index=True, unique=True)
    password_hash: orm.Mapped[Optional[str]] = orm.mapped_column(alchemy.String(256)) # 16-тиричное число хранящее пароль в виде цифр и букв
    posts: orm.WriteOnlyMapped['Post'] = orm.relationship(back_populates="author")
    about_me: orm.Mapped[Optional[str]] = orm.mapped_column(alchemy.String(256)) # биография
    last_seen: orm.Mapped[Optional[datetime]] = orm.mapped_column(default=lambda:datetime.now(timezone.utc)) # указание времени последнего посещения
    question: orm.Mapped[str] = orm.mapped_column(alchemy.String(64), index=True)
    answer: orm.Mapped[str] = orm.mapped_column(alchemy.String(64), index=True)


    def __repr__(self):
        return f"User: {self.username, self.email}"
    

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)


    def check_password(self, password):
        return check_password_hash(self.password_hash, password)
    

    def avatar(self, size):
        image = md5(self.email.lower().encode("utf-8")).hexdigest()
        return f"https://www.gravatar.com/avatar/{image}? if d = identicon&s={size}"

class Post(db.Model):
    id: orm.Mapped[int] = orm.mapped_column(primary_key=True)
    post_title: orm.Mapped[str] = orm.mapped_column(alchemy.String(70))
    post_body: orm.Mapped[str] = orm.mapped_column(alchemy.String(5000))
    date_created: orm.Mapped[datetime] = orm.mapped_column(default=lambda:datetime.now(timezone.utc), index=True) # указание времени конкретного поста
    user_id: orm.Mapped[int] = orm.mapped_column(alchemy.ForeignKey(User.id), index=True)
    author: orm.Mapped["User"] = orm.relationship(back_populates="posts")

    def __repr__(self):
        return f"Post: {self.post_title, self.date_created}"
    

    def set_body(self, new_body):
        self.post_body = new_body


    def get_body(self):
        return self.post_body

    
@login.user_loader
def load_user(id):
    return db.session.get(User, int(id))


class Component(db.Model):
    id: orm.Mapped[int] = orm.mapped_column(primary_key=True)
    component_title: orm.Mapped[str] = orm.mapped_column(alchemy.String(70))
    component_body: orm.Mapped[str] = orm.mapped_column(alchemy.String(500))
    component_type: orm.Mapped[str] = orm.mapped_column(alchemy.String(50))


    def set_body(self, new_body):
        self.component_body = new_body


    def get_body(self):
        return self.component_body