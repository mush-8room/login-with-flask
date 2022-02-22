from flask_wtf import FlaskForm
from wtforms import StringField, validators, PasswordField, BooleanField


class RegistrationForm(FlaskForm):
    username = StringField('Username', [validators.Length(min=4, max=25)])
    password = PasswordField('New Password', [
        validators.DataRequired(),
        validators.EqualTo('password_confirm', message='Passwords must match')
    ])
    password_confirm = PasswordField('Repeat Password')
    accept_tos = BooleanField('I accept the TOS', [validators.InputRequired()])