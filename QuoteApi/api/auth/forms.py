from flask_wtf import FlaskForm
from wtforms import PasswordField, StringField
from wtforms.validators import EqualTo, InputRequired


class RegistrationForm(FlaskForm):
    username = StringField("Username", [InputRequired()])
    password = PasswordField(
        "Password",
        [InputRequired(), EqualTo("confirm", message="Passwords must match")]
    )
    confirm = PasswordField("Confirm password", [InputRequired()])


class LoginForm(FlaskForm):
    username = StringField("Username", [InputRequired()])
    password = PasswordField("Password", [InputRequired()])
