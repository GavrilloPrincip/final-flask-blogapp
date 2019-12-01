from blog import app
from flask import render_template, redirect, url_for
from blog.forms import LoginForm, RegisterForm

@app.route("/")
@app.route("/home")
def home():
    title = "HOME"
    return render_template('public/home.html', title = title)

@app.route("/register")
def register():
    form = RegisterForm()
    title = "REGİSTER"
    return render_template("public/register.html", title = title, form = form)

@app.route("/login")
def login():
    form = LoginForm()
    title = "LOGİN"
    return render_template("public/login.html", title = title, form = form)