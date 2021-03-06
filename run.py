from flask import Flask, render_template, request, redirect, url_for
from forms import *
from flask_login import LoginManager, current_user, login_user, logout_user, login_required
from models import *
from werkzeug.urls import url_parse

app = Flask(__name__)
'''
Parámetros de configuración a nivel de apliación
'''
app.config['SECRET_KEY'] = '7110c8ae51a4b5af97be6534caef90e4bb9bdcb3380af008f90b23a5d1616bf319bc298105da20f'

'''Instancia de la clase LoginManager'''
login_manager = LoginManager(app)
login_manager.login_view = "login"

posts = []


@app.route('/') #URL a la página principal
def index():
    return render_template("index.html", num_posts=posts)

@app.route('/p/<string:slug>/')
def show_post(slug):
    return render_template("post_view.html", slug_title=slug)

'''Dos URL para la misma vista'''
@app.route("/admin/post/")
@app.route("/admin/post/<int:post_id>")
@login_required # Protección de esta vista a usuarios autenticados
def post_form(post_id):
    form = PostForm()
    if form.validate_on_submit():
        title = form.title.data
        title_slug = form.title_slug.data
        content = form.content.data
        post = {'title': title, 'title_slug': title_slug, 'content': content}
        posts.append(post)
        return redirect(url_for('index'))
    return render_template("admin/post_form.html", form=form)

'''
Vista para el formulario de registro de usuarios
'''
@app.route("/signup/", methods=["GET", "POST"])
def show_signup_form():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = SignupForm()
    if form.validate_on_submit():
        name = form.name.data
        email = form.email.data
        password = form.password.data
        # Creamos el usuario y lo guardamos
        user = User(len(users) + 1, name, email, password)
        users.append(user)
        # Dejamos al usuario logueado
        login_user(user, remember=True)
        next_page = request.args.get('next', None)
        if not next_page or url_parse(next_page).netloc != '':
            next_page = url_for('index')
        return redirect(next_page)
    return render_template("signup_form.html", form=form)

@login_manager.user_loader
def load_user(user_id):
    for user in users:
        if user.id == int(user_id):
            return user
    return None


'''
Vista para realizar el login
'''
from werkzeug.urls import url_parse

@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated: # El usuario ya está autenticado?
        return redirect(url_for('index'))
    form = LoginForm()
    if form.validate_on_submit():
        user = get_user(form.email.data)
        if user is not None and user.check_password(form.password.data):
            login_user(user, remember=form.remember_me.data)
            next_page = request.args.get('next')
            if not next_page or url_parse(next_page).netloc != '':
                next_page = url_for('index')
            return redirect(next_page)
    return render_template('login_form.html', form=form)


'''
Vista para cerrar la sesión 'logout'
'''

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))