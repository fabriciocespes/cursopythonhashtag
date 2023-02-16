from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
import os

app = Flask(__name__)


app.config['SECRET_KEY'] = '691f1580414a0bfc0525ad6d32f53563exit'

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgres://comunidade_user:6XhFUjPGwXARH8jR5Gmio0jsGzM0UJGA@dpg-cfn82tirrk0eqlv60300-a.oregon-postgres.render.com/comunidade'

database = SQLAlchemy(app)
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'
login_manager.login_message_category = 'alert-info'

from comunidadeimpressionadora import routes
