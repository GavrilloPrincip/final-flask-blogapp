from flask_wtf import FlaskForm
from wtforms import validators, StringField, PasswordField, BooleanField, ValidationError, SubmitField, FileField, TextAreaField
from wtforms.validators import DataRequired, Email, EqualTo, Length
from blog.models import User
from flask_login import current_user
from flask_wtf.file import FileRequired, FileAllowed
from flask import request

class RegisterForm(FlaskForm):
    username = StringField("Username", validators=[DataRequired(), Length(min = 4, max = 10)])
    email = StringField("E-mail", validators=[DataRequired(), Email()])
    password = PasswordField("Password", validators=[DataRequired(), Length(min = 8, max= 16)])
    confirmpassword = PasswordField(validators=[EqualTo('password')])
    def validate_username(self, username):
        if User.query.filter_by(username = username.data).first():
            raise ValidationError("Bu kullanıcı adı alınmış!")
    def validate_email(self, email):
        if User.query.filter_by(email = email.data).first():
            raise ValidationError("Bu email adresi alınmış!")   



class LoginForm(FlaskForm):
    email = StringField("Email")
    password = PasswordField("Password")
    rememberme = BooleanField("Remember me")


class UpdateForm(FlaskForm):
    username = StringField("username", validators=[DataRequired() ,Length(min=4, max=10)])
    email = StringField("email", validators=[DataRequired(), Email()])
    submit = SubmitField("Update")
    
    def validate_username(self,username):
        if current_user.username == username.data:
            raise ValidationError("Şuanki kullanıcı adınızla aynı olamaz")
    
    def validate_email(self,email):
        if current_user.email == email.data:
            raise ValidationError("Şuanki Email adresinizle aynı olamaz.")

class AvatarForm(FlaskForm):
    avatar = FileField('Avatar', validators=[FileRequired(), FileAllowed(['jpg', 'png'])])
    submit = SubmitField('Update')
    
    def validate_avatar(self,avatar):
        if request.content_length > 3* 1024 * 1024:
            raise ValidationError("Fotoğraf 3M den büyük olamaz")

class NewArticleForm(FlaskForm):
    title = StringField("Title",validators=[ DataRequired()])
    content = TextAreaField("content", validators=[DataRequired()])

class NewCommentForm(FlaskForm):
    comment = TextAreaField("comment", validators=[DataRequired()])
    submit = SubmitField('new comment')