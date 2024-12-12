from collections.abc import Sequence
from typing import Any, Mapping
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, TextAreaField, SelectField
from wtforms.validators import DataRequired, Email, EqualTo, ValidationError, Length
from app import db
from app.models import User
import sqlalchemy as alcemy

component_types = [("sitebar component", "sitebar component"), ("blog name", "blog name"), ("socialbar", "socialbar")]

class LoginForm(FlaskForm):
    username = StringField("Username", validators=[DataRequired()])
    password = PasswordField("Password", validators=[DataRequired()])
    remember_me = BooleanField("Remember Me")
    submit = SubmitField("Log in")

class Registration(FlaskForm):
    username = StringField("Username", validators=[DataRequired()])
    email = StringField("Email", validators=[DataRequired(), Email()])
    password = PasswordField("Password", validators=[DataRequired()])
    password_2 = PasswordField("Repeat Password", validators=[DataRequired(), EqualTo("password")])
    submit = SubmitField("Register")

    def validate_username(self, username):
        user = db.session.scalar(alcemy.select(User).where(User.username == username.data))
        if user is not None:
            raise ValidationError("Please chouse a different username.")

    def validate_email(self, email):
        user = db.session.scalar(alcemy.select(User).where(User.email == email.data))
        if user is not None:
            raise ValidationError("Please chouse a different email.")

class PostEditor(FlaskForm):
    post_title = StringField("Title", validators=[DataRequired(), Length(min=5, max=75)])
    post_body = TextAreaField("Text", validators=[Length(min=0, max=5000)])
    submit = SubmitField("Save")


class ComponentEditor(FlaskForm):
    component_title = StringField("Title", validators=[DataRequired(), Length(min=5, max=75)])
    component_body = TextAreaField("Text", validators=[Length(min=0, max=5000)])
    component_type = SelectField("Type", choices=component_types)
    submit = SubmitField("Save")