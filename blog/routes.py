from blog import app, db
from flask import render_template, redirect, url_for, flash, request, abort
from blog.forms import LoginForm, RegisterForm, UpdateForm, AvatarForm, NewArticleForm, NewCommentForm
from werkzeug.security import generate_password_hash, check_password_hash
from blog.models import User, Post, Comment, ReComment
from flask_login import current_user, login_user, logout_user, login_required
from werkzeug.urls import url_parse
from werkzeug.utils import secure_filename
import os
from datetime import datetime


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
    if current_user.is_authenticated:
        flash("Zaten kullanıcı girişi yaptınız!","danger")
        return redirect(url_for('home'))

    form = LoginForm()
    if form.validate_on_submit():
        current_user
        user = User.query.filter_by(email = form.email.data).first()
        if user != None:
            if check_password_hash(user.password, form.password.data):
                login_user(user, remember=form.rememberme.data)
                next_page = request.args.get('next')
                if not next_page or url_parse(next_page).netloc != '':
                    next_page = url_for('home')
                flash("Giriş Başarılı", "success")
                return redirect(next_page)
            else:
                flash('Check your details', 'danger')
        else:
            flash('check your details', 'danger')
            
    title = "LOGİN"
    return render_template("public/login.html", title = title, form = form)

@app.route("/logout")
def logout():
    logout_user()
    flash("Başarıyla çıkış yaptınız","success")
    return redirect(url_for('home'))


@app.route("/user/<username>",methods = ['GET','POST'])
def profil(username):
    user = User.query.filter_by(username=username).first_or_404()
    form1 = UpdateForm()
    avatar = user.avatar
    img_src = url_for('static',filename = 'img/userpic/' + avatar)
    form2 = AvatarForm()
    posts = Post.query.filter_by(user_id = user.id).all()
    posts = tuple(posts)
    return render_template('admin/account.html',img_src = img_src, form1 = form1, form2 = form2, user = user, posts = posts)

@app.route("/updateImage", methods = ['POST'])
def upImage():
    form2 = AvatarForm()
    form1 = UpdateForm()
    img_src = url_for('static',filename = 'img/userpic/' + current_user.avatar)
    if form2.validate_on_submit():
        flash("Fotoğraf kaydedildi","success")
        file = form2.avatar.data
        filename = secure_filename(form2.avatar.data.filename)
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        current_user.avatar = filename
        db.session.commit()
        return redirect(url_for("profil", username = current_user.username))
    else:
        flash("Fotoğraf kaydetyme başarısız","danger")
        return render_template("admin/account.html", img_src = img_src, form2 = form2, form1 = form1)

@app.route("/updateDetails", methods = ['POST'])
def upDetails():
    form1 = UpdateForm()
    form2 = AvatarForm()
    img_src = url_for('static',filename = 'img/userpic/' + current_user.avatar)
    if form1.validate_on_submit:
        current_user.username = form1.username.data
        current_user.email = form1.email.data
        db.session.commit()
        flash("Değişiklikler kaydedildi","success")
        return redirect(url_for("profil", username = current_user.username))
    else:
        flash("Değişiklikler kaydedilemedi","danger")
        return render_template("admin/account.html", img_src = img_src, form1 = form1, form2 = form2)


@app.route("/newarticle", methods = ['GET','POST'])
@login_required
def newarticle():
    form = NewArticleForm()
    if form.is_submitted():
        if form.validate():
            title = form.title.data
            content = form.content.data
            post = Post(title = title, content = content, user_id = current_user.id)
            db.session.add(post)
            db.session.commit()
            flash("Article oluşturuldu","success")
            return redirect(url_for("profil",username = current_user.username))
        else:
            flash("Hata","danger")
    return render_template("admin/newarticle.html", form = form, title="newarticle")
    
    
@app.before_request
def before_request():
    if current_user.is_authenticated:
        current_user.last_seen = datetime.utcnow()
        db.session.commit()

@app.route("/article/<article>", methods = ['GET', 'POST'])
def show_article(article):
    post = Post.query.filter_by(id = article).first_or_404()
    form = NewCommentForm()
    if form.validate_on_submit():
        content = form.comment.data
        comment = Comment(content = content,post_id  = post.id, user_id = current_user.id)
        db.session.add(comment)
        db.session.commit()
        flash('Comment added','success')
        return redirect(url_for('show_article',article = post.id))
    comments = Comment.query.filter_by(post_id = post.id).all()
    recomments = ReComment.query.all() 
    return render_template("public/article.html", post = post, comments = comments, form = form, recomments = recomments)

@app.route("/updatearticle/<article>",methods = ['GET','POST'])
@login_required
def update_article(article):
    post = Post.query.filter_by(id = article).first_or_404()
    if current_user.id != post.user_id or post == None:
        abort(403)

    form = NewArticleForm()
    form.title.data = post.title
    form.content.data = post.content
    if form.is_submitted():
        if form.validate():
            post.title = form.title.data
            post.content = form.content.data
            flash("değişiklikler kaydedildi","sucecss")
            return redirect(url_for('show_article',article = post.id))
        else:
            flash("Hata!","danger")
    return render_template("admin/newarticle.html", form = form, title = 'updatearticle')

@app.route("/deletearticle/<article>")
@login_required
def delete_article(article):
    post = Post.query.filter_by(id = article).first_or_404()
    if current_user.id != post.user_id:
        abort(403)
    db.session.delete(post)
    db.session.commit()
    return redirect(url_for("profil",username = current_user.username))    

@app.route("/posts")
def posts():
    posts = Post.query.all()
    return render_template("public/posts.html", posts = posts)

@app.route("/follow/<username>")
@login_required
def follow(username):
    user = User.query.filter_by(username = username).first_or_404()
    if user == current_user:
        flash("kendinle takipleşemezsin","danger")
    else:
        current_user.followers.append(user)
        db.session.commit()
        flash("kullanıcı artık takip ediliyor","success")
    return redirect(url_for("profil",username = user.username))

@app.route("/unfollow/<username>")
@login_required
def unfollow(username):
    user = User.query.filter_by(username = username).first_or_404()
    if user == current_user:
        flash("kendinle takipleşemezsin","danger")
    else:
        current_user.followers.remove(user)
        db.session.commit()
        flash("Kullanıcı takipten çıkarıldı","success")
    return redirect(url_for("profil",username = username))
        

@app.route("/comment/<comment>/recomment",methods = ['POST'])
@login_required
def recomment(comment):
    form = NewCommentForm()
    comment = Comment.query.filter_by(id = comment).first()
    if form.validate_on_submit():
        content = form.comment.data
        recomment = ReComment(content = content, comment_id = comment.id , user_id = current_user.id)
        db.session.add(recomment)
        db.session.commit()
        flash("cevap eklendi","success")
        return redirect(url_for("show_article",article = comment.topost.id))





