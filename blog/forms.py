from flask_wtf import FlaskForm
from wtforms import validators, StringField, PasswordField, BooleanField
from wtforms.validators import DataRequired, Email, EqualTo, Length

class RegisterForm(FlaskForm):
    username = StringField("Username", validators=[DataRequired(), Length(min = 4, max = 10)])
    email = StringField("E-mail", validators=[DataRequired(), Email])
    password = PasswordField("Password", validators=[DataRequired(), Length(min = 8, max= 16)])
    confirmpassword = PasswordField(validators=[EqualTo('password')])

class LoginForm(FlaskForm):
    email = StringField("Email")
    password = PasswordField("Password")
    rememberme = BooleanField("Remember me")