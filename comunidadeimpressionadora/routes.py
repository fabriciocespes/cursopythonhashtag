from flask import render_template, redirect, url_for, flash, request, abort
from comunidadeimpressionadora import app, database
from comunidadeimpressionadora.forms import FormLogin, FormCriarConta, FormEditarPerfil, FormCriarPost
from comunidadeimpressionadora.models import Usuario, Post
from flask_login import login_user, logout_user, current_user, login_required
import secrets
import os
from PIL import Image
import bcrypt
import hashlib

@app.route('/')
def home():
    # em ordem decrescente
    posts = Post.query.order_by(Post.id.desc())
    return render_template('home.html', posts=posts)


@app.route('/contato')
def contato():
    return render_template('contato.html')


@app.route('/usuarios')
@login_required
def usuarios():
    lista_usuarios = Usuario.query.all()
    return render_template('usuarios.html', lista_usuarios=lista_usuarios)


@app.route('/login', methods=['GET', 'POST'])
def login():
    form_login = FormLogin()
    form_criarconta = FormCriarConta()


    # Formulário de Login

    if form_login.validate_on_submit() and 'botao_submit_login' in request.form:
        usuario = Usuario.query.filter_by(email=form_login.email.data).first()

        # compara se o usuario existe e se a senha que foi preenchida no formulário bate com a do banco de dados.
        # if usuario and bcrypt.check_password_hash(usuario.senha, form_login.senha.data):
        # inseri o bcrypt.hashpw para funcionar no servidor Render.com
        senha_form = form_login.senha.data
        senha_form = hashlib.sha256(senha_form.encode('utf-8')).hexdigest()
        if usuario and bcrypt.hashpw(senha_form.encode('utf-8'), usuario.senha):
            login_user(usuario, remember=form_login.lembrar_dados.data)
            flash(f'Login feito com sucesso no e-mail: {form_login.email.data}', 'alert-success')
            # pega o parâmetro do link e direciona para a url next
            par_next = request.args.get('next')
            if par_next:
                return redirect(par_next)
            else:
                return redirect(url_for('home'))
        else:
            flash(f'Falha no Login. E-mail ou senha Incorretos : {form_login.email.data}', 'alert-danger')

    # Formulário Criar Conta
    if form_criarconta.validate_on_submit() and 'botao_submit_criarconta' in request.form:
        # senha_cript = bcrypt.generate_password_hash(form_criarconta.senha.data)
        # inseri o bcrypt.hashpw para funcionar no servidor Render.com

        senha_cript = bcrypt.hashpw(form_criarconta.senha.data.encode('utf-8'), bcrypt.gensalt())


        usuario = Usuario(username=form_criarconta.username.data, email=form_criarconta.email.data, senha=senha_cript)
        database.session.add(usuario)
        database.session.commit()
        flash(f'Conta criada para o e-mail: {form_criarconta.email.data}', 'alert-success')
        return redirect(url_for('home'))
    return render_template('login.html', form_login=form_login, form_criarconta=form_criarconta)

@app.route('/sair')
@login_required
def sair():
    logout_user()
    flash(f'Logout Feito com Sucesso.', 'alert-success')
    return redirect(url_for('login'))

@app.route('/perfil')
@login_required
def perfil():
    foto_perfil = url_for('static', filename='fotos_perfil/{}'.format(current_user.foto_perfil))
    return render_template('perfil.html', foto_perfil=foto_perfil)

@app.route('/post/criar', methods=['GET', 'POST'])
@login_required
def criar_post():
    form = FormCriarPost()
    if form.validate_on_submit():
        post = Post(titulo=form.titulo.data, corpo=form.corpo.data, autor=current_user)
        database.session.add(post)
        database.session.commit()
        flash('Post Criado com Sucesso...', 'alert-success')
        return redirect(url_for('home'))
    return render_template('criarpost.html', form=form)

def salvar_imagem(imagem):
    # adicionar um código aleatório ao nome da imagem (importar biblioteca secrets e os)
    codigo = secrets.token_hex(8)

    # pegando o nome do arquivo de imagem e separando o nome da extensão e guardando nas variáveis nome e extensao
    nome, extensao = os.path.splitext(imagem.filename)
    nome_arquivo = nome + codigo + extensao
    caminho_completo = os.path.join(app.root_path, 'static/fotos_perfil', nome_arquivo)

    # reduzir o tamanho da imagem é preciso instalar o Pillow e importar PIL->Image
    tamanho = (400, 400)
    imagem_reduzida = Image.open(imagem)
    imagem_reduzida.thumbnail(tamanho)

    # salvar a imagem na pasta fotos_perfil
    imagem_reduzida.save(caminho_completo)

    # mudar o campo foto_perfil do usuário para o novo nome da imagem
    return nome_arquivo

def atualizar_cursos(form):
    lista_cursos = []
    for campo in form:
        if 'curso_' in campo.name:
            # retorna False ou True se o campo estiver marcado
            if campo.data:
                # adicionar o texto do campo.label na lista de cursos
                lista_cursos.append(campo.label.text)
    # Vai ter uma lista como resultado no fim do for, mas precisa armazenar como String no banco de dados
    # (O método join é usado para transformar a lista em String - vai percorrer toda a lista e juntar o texto separando por ';')
    return ';'.join(lista_cursos)


@app.route('/perfil/editar', methods=['GET', 'POST'])
@login_required
def editar_perfil():
    form = FormEditarPerfil()
    if form.validate_on_submit():
        current_user.email = form.email.data
        current_user.username = form.username.data
        if form.foto_perfil.data:
            # chamando a função salvar_imagem
            nome_imagem = salvar_imagem(form.foto_perfil.data)
            current_user.foto_perfil = nome_imagem

        # chamando a função atualizar_cursos para preencher os cursos marcados no formulário
        # inseri esse if por minha conta quando atualizava somente a foto os cursos zeravam
        if form.curso_excel.data or form.curso_powerbi.data or form.curso_ppt.data or form.curso_sql.data or form.curso_vba.data or form.curso_python.data:
            current_user.cursos = atualizar_cursos(form)

        database.session.commit()
        flash(f'Perfil atualizado com sucesso.', 'alert-success')
        return redirect(url_for('perfil'))
    elif request.method == "GET":
        form.email.data = current_user.email
        form.username.data = current_user.username
    foto_perfil = url_for('static', filename='fotos_perfil/{}'.format(current_user.foto_perfil))
    return  render_template('editarperfil.html', foto_perfil=foto_perfil, form=form)

# criando uma página dinâmica
@app.route('/post/<post_id>', methods=['GET', 'POST'])
@login_required
def exibir_post(post_id):
    post = Post.query.get(post_id)
    # para editar o post caso o mesmo seja do usuario logado
    if current_user == post.autor:
        # vai usar o FormCriarPost pois o mesmo já tem tudo qque se necessita para editar o post, sem necessidade de criar um novo formulário EditarPost
        form = FormCriarPost()
        # atribuindo os valores do post as caixas para o usuario só editar o que for necessário
        if request.method == 'GET':
            form.titulo.data = post.titulo
            form.corpo.data = post.corpo
        # aqui eu edito o post
        elif form.validate_on_submit():
            post.titulo = form.titulo.data
            post.corpo = form.corpo.data
            # nao precisa do database.add poqqrque esse post já existe
            database.session.commit()
            flash('Post Atualizado com Sucesso', 'alert-success')
            return redirect(url_for('home'))
    else:
        form = None
    return render_template('post.html', post=post, form=form)

# Excluindo o post

@app.route('/post/<post_id>/excluir', methods=['GET', 'POST'])
@login_required
def excluir_post(post_id):
    post = Post.query.get(post_id)
    # só pode excluir quem for o dono do post
    if current_user == post.autor:
        database.session.delete(post)
        database.session.commit()
        flash('Post Excluído com Sucesso', 'alert-danger')
        return redirect(url_for('home'))
    else:
        # import abort
        abort(403)
