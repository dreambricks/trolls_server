from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user
from flask import render_template, redirect, url_for, request, Blueprint
from mongo_setup import db

login_manager = LoginManager()
auth = Blueprint('auth', __name__)


class User(UserMixin):
    def __init__(self, username):
        self.username = username

    def get_id(self):
        return self.username


@login_manager.user_loader
def load_user(username):
    user_data = db.users.find_one({'_id': username})
    if not user_data:
        return None
    return User(username)


@auth.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        # Verificar se o nome de usuário já existe no banco de dados
        if db.users.find_one({'_id': username}):
            return 'Nome de usuário já existe. Escolha outro nome de usuário.'

        # Inserir o novo usuário no banco de dados
        db.users.insert_one({'_id': username, 'password': password})
        return 'Cadastro realizado com sucesso. <a href="/">Ir para a página inicial</a>'

    return render_template('register.html')


@auth.route('/login', methods=['POST'])
def do_login():
    username = request.form['username']
    password = request.form['password']
    user_data = db.users.find_one({'_id': username})
    if user_data and user_data['password'] == password:
        user = User(username)
        login_user(user)
        return redirect(url_for('home'))
    return 'Login inválido.'


@auth.route('/login')
def login():
    return render_template('login.html')


@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('home'))
