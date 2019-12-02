from blog import app, db
from flask import render_template, redirect, url_for, flash
from blog.forms import LoginForm, RegisterForm
from werkzeug.security import generate_password_hash, check_password_hash
from blog.models import User, Post
@app.route("/")
@app.route("/home")
def home():
    title = "HOME"
    return render_template('public/home.html', title = title)

@app.route("/register", methods=["GET","POST"])
def register():
    form = RegisterForm()
    title = "REGİSTER"
    if form.validate_on_submit():
        username = form.username.data
        email = form.email.data
        password = form.password.data
        hash_pass = generate_password_hash(password)
        user = User(username = username, email = email, password = hash_pass)
        db.session.add(user)
        db.session.commit()
        flash("The account existed for {}".format(username),"success")
        return redirect(url_for("login"))
    return render_template("public/register.html", title = title, form = form)

@app.route("/login", methods = ["GET","POST"])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email = form.email.data).first()
        if user != None:
            if check_password_hash(user.password, form.password.data):
                flash("Giriş Başarılı", "success")
                return redirect(url_for('home'))
    title = "LOGİN"
    return render_template("public/login.html", title = title, form = form)