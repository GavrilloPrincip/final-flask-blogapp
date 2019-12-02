from blog import db
from datetime import datetime

class User(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    username = db.Column(db.String(30), unique = True, index = True)
    email = db.Column(db.String(30), unique = True, index = True)
    password = db.Column(db.String(200))
    posts = db.relationship('Post', backref = 'author', lazy = True)
    def __repr__(self):
        return "user id:{}, username:{}, email:{}".format(self.id, self.username, self.email)

class Post(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    title = db.Column(db.String(30), unique = True, index = True)
    content = db.Column(db.String(1000), index = True)
    post_time = db.Column(db.DateTime, index = True, default = datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    def __repr__(self):
        return "post id:{}, title:{}".format(self.id, self.title)