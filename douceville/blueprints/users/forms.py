from flask_wtf import FlaskForm
from wtforms.fields import SelectField
from wtforms.fields import StringField, SubmitField, FloatField, PasswordField
from wtforms.validators import DataRequired, Email

from douceville.models import *


class LoginForm(FlaskForm):
    email = StringField("Email", validators=[DataRequired(), Email()])
    password = PasswordField("Password", validators=[DataRequired()])

    submit = SubmitField("Login")


class SignupForm(FlaskForm):
    email = StringField("Email", validators=[DataRequired(), Email()])
    password = PasswordField("Password", validators=[DataRequired()])

    submit = SubmitField("Sign up")
