from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
import os
import sqlalchemy

app = Flask(__name__)


app.config['SECRET_KEY'] = '691f1580414a0bfc0525ad6d32f53563exit'

# if os.getenv("DATABASE_URL"):
#     app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv("DATABASE_URL")
# else:
#     app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///comunidade.db'
app.config['SQLALCHEMY_DATABASE_URI'] = "postgres://comunidade_ktu9_user:HFDdVcjFSvieNvhnB2fHFtQMCl21y0jz@dpg-cfo24birrk0239gabavg-a.oregon-postgres.render.com/comunidade_ktu9"
# postgres://comunidade_ktu9_user:HFDdVcjFSvieNvhnB2fHFtQMCl21y0jz@dpg-cfo24birrk0239gabavg-a.oregon-postgres.render.com/comunidade_ktu9


database = SQLAlchemy(app)
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'
login_manager.login_message_category = 'alert-info'

# from comunidadeimpressionadora import models
# 
# engine = sqlalchemy.create_engine(app.config['SQLALCHEMY_DATABASE_URI'])
# 
# if not engine.has_table("usuario"):
#     with app.app_context():
#         database.drop_all()
#         database.create_all()
#         print('Base de Dados Criada')
# else:
#     print('Base de Dados Existente')

from comunidadeimpressionadora import routes
