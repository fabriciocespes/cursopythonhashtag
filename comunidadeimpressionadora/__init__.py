from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
import os
import sqlalchemy as sa

app = Flask(__name__)


app.config['SECRET_KEY'] = '691f1580414a0bfc0525ad6d32f53563exit'

if os.getenv("DATABASE_URL"):
    app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv("DATABASE_URL")
else:
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///comunidade.db'
# app.config['SQLALCHEMY_DATABASE_URI'] = "postgres://comunidade_dbj7_user:ud9ADfi1mCioBDCnNtvBg53fotcFntf5@dpg-cfoh9e14rebfdaopa3jg-a.oregon-postgres.render.com/comunidade_dbj7"

database = SQLAlchemy(app)
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'
login_manager.login_message_category = 'alert-info'

from comunidadeimpressionadora import models

engine = sa.create_engine(app.config['SQLALCHEMY_DATABASE_URI'])
insp = sa.inspect(engine)

if not sa.engine.reflection.Inspector.has_table(insp, 'usuario'):
    with app.app_context():
        database.drop_all()
        database.create_all()
        print('Base de Dados Criada')
else:
    print('Base de Dados Existente')

from comunidadeimpressionadora import routes
