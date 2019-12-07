from blog import db, login
from datetime import datetime
from flask_login import UserMixin

@login.user_loader # Kullanıcının giriş yapması!
def load_user(id):
    return User.query.get(id)


followers = db.Table(
    'followers',
    db.Column('follower_id', db.Integer, db.ForeignKey('user.id')),
    db.Column('followed_id', db.Integer, db.ForeignKey('user.id'))
)

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key = True)
    username = db.Column(db.String(30), unique = True, index = True)
    email = db.Column(db.String(30), unique = True, index = True)
    password = db.Column(db.String(200))
    avatar = db.Column(db.String(100), default ='default.png')
    posts = db.relationship('Post', backref = 'author', lazy = True)
    comments = db.relationship('Comment', backref = 'author', lazy = True)
    recomments = db.relationship('ReComment', backref = 'author', lazy = True)
    last_seen = db.Column(db.DateTime, default = datetime.utcnow)
    followed = db.relationship(
        'User', secondary=followers,
        primaryjoin=(followers.c.follower_id == id),
        secondaryjoin=(followers.c.followed_id == id),
        backref=db.backref('followers', lazy='dynamic'), lazy='dynamic')
    def __repr__(self):
        return "user id:{}, username:{}, email:{}".format(self.id, self.username, self.email)

class Post(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    title = db.Column(db.String(30), unique = True, index = True)
    content = db.Column(db.String(1000), index = True)
    post_time = db.Column(db.DateTime, index = True, default = datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    comments = db.relationship('Comment', backref = 'topost', lazy = True)

    def __repr__(self):
        return "post id:{}, title:{}".format(self.id, self.title)

class Comment(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    content = db.Column(db.String(100), index = True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    post_id = db.Column(db.Integer, db.ForeignKey('post.id'))
    recomments = db.relationship('ReComment', backref = 'tocomment', lazy = True)
    def __repr__(self):
        return "comment id:{}, authorid:{}, post.id:{}".format(self.id, self.user_id, self.post_id)

class ReComment(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    content = db.Column(db.String(100), index = True)
    comment_id = db.Column(db.Integer, db.ForeignKey('comment.id'))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    def __repr__(self):
        return "recommentid:{}, commentid:{}".format(self.id,self.comment_id)
    
