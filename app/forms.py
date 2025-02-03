from collections.abc import Sequence
from typing import Any, Mapping
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, TextAreaField, SelectField
from wtforms.validators import DataRequired, Email, EqualTo, ValidationError, Length
from app import db
from app.models import User
import sqlalchemy as alcemy

component_types = [("sitebar component", "sitebar component"), ("blog name", "blog name"), ("socialbar", "socialbar")]
questions = [("whot is your favorite song?", "whot is your favorite song?"), ("whot is your favorite movie?", "whot is your favorite movie?"), ("whot is your favorite writer?", "whot is your favorite writer?"), ("How is your favorite actor?", "How is your favorite actor?"), ("whot is your favorite animal?", "whot is your favorite animal?")]

class LoginForm(FlaskForm):
    username = StringField("Username", validators=[DataRequired(message="Wrong username or password"), Length(min = 1, max = 50, message="Wrong username or password")])
    password = PasswordField("Password", validators=[DataRequired(message="Wrong username or password"), Length(min = 1, max = 50, message="Wrong username or password")])
    remember_me = BooleanField("Remember Me")
    submit = SubmitField("Log in")

class Registration(FlaskForm):
    username = StringField("Username", validators=[DataRequired()])
    email = StringField("Email", validators=[DataRequired(), Email()])
    password = PasswordField("Password", validators=[DataRequired()])
    password_2 = PasswordField("Repeat Password", validators=[DataRequired(), EqualTo("password")])
    question = SelectField("Question", choices=questions)
    answer = StringField("Answer", validators=[DataRequired()])
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
    post_title = StringField("Title", validators=[DataRequired(), Length(min=5, max=75, message="Text must be from 5 to 75")])
    post_body = TextAreaField("Text", validators=[Length(min=0, max=5000, message="Text is too long")])
    submit = SubmitField("Save")


class ComponentEditor(FlaskForm):
    component_title = StringField("Title", validators=[DataRequired(), Length(min=5, max=75, message="Text must be from 5 to 75")])
    component_body = TextAreaField("Text", validators=[Length(min=0, max=5000, message="Text is too long")])
    component_type = SelectField("Type", choices=component_types)
    submit = SubmitField("Save")


class GetReset(FlaskForm):
    username = StringField("Username", validators=[DataRequired()])
    submit = SubmitField("Next")


class PasswordResetForm(FlaskForm):
    password = PasswordField("New Password", validators=[DataRequired()])
    password_2 = PasswordField("Repeat New Password", validators=[DataRequired(), EqualTo("password")])
    answer = StringField("Answer", validators=[DataRequired()])
    submit = SubmitField("Reset Password")