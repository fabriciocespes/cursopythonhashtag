from comunidadeimpressionadora import database, login_manager
from datetime import datetime
# Parâmetro que passamos para a classe Usuario que vai atribuir a ela todas as características
# que o LoginManager precisa para ele conseguir controlar o login, manter o login conectado etc
from flask_login import UserMixin

# Processo padrão
# Função para encontrar um usuario com o id definido
# o get já encontra pela chave primária
@login_manager.user_loader
def load_usuario(id_usuario):
    return Usuario.query.get(int(id_usuario))


class Usuario(database.Model, UserMixin):
    id = database.Column(database.Integer, primary_key=True)
    username = database.Column(database.String, nullable=False)
    email = database.Column(database.String, nullable=False, unique=True)
    senha = database.Column(database.String, nullable=False)
    foto_perfil = database.Column(database.String, default='default.jpg')
    posts = database.relationship('Post', backref='autor', lazy=True)
    cursos = database.Column(database.String, nullable=False, default='Não Informado')

    # Criando um método exclusivo da Classe usuario para contar seus Posts
    def contar_posts(self):
        return len(self.posts)


class Post(database.Model):
    id = database.Column(database.Integer, primary_key=True)
    titulo = database.Column(database.String, nullable=False)
    corpo = database.Column(database.Text, nullable=False)
    data_criacao = database.Column(database.DateTime, nullable=False, default=datetime.utcnow)
    id_usuario = database.Column(database.Integer, database.ForeignKey('usuario.id'), nullable=False)