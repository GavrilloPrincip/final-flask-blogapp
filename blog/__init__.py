from flask import Flask

app = Flask(__name__)
app.secret_key = "you can't find"

from blog import routes