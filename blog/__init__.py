from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
import os
from flask_migrate import Migrate

app = Flask(__name__, static_folder='static', template_folder='templates')

app.config['SECRET_KEY'] = "you can't find"
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:''@localhost/blog'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['UPLOAD_FOLDER'] = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'static/img/userpic')

db = SQLAlchemy(app)
migrate = Migrate(app, db)
login = LoginManager(app)

from blog import routes