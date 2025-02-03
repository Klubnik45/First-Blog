from flask import render_template, flash, redirect, url_for, request # импорт функций из пакета flask (render_template - принимает имя шаблона и список переменных аргументов шаблона и возвращает готовый шаблон с заменёнными аргументами, flash — используется для отображения временных сообщений пользователю после выполнения определённого запроса, redirect — позволяет перенаправлять пользователей на указанный URL и присваивать указанному коду состояния, url_for - генерация URL)
from app import app, db # импорт переменных
from app.forms import LoginForm, Registration, PostEditor, ComponentEditor, GetReset, PasswordResetForm # импорт классов (LoginForm - реализует представление окна входа в систему, Registration - сохранение ссылки на объект одного класса в другом, PostEditor - редактирует сообщения)
from flask_login import current_user, login_user, logout_user, login_required # Flask-Login — это расширение Flask, которое управляет состоянием входа пользователя в систему.
from app.models import User, Post, Component
from markdown_processer import *
import sqlalchemy as alchemy


def get_html(markdown):
    for p in markdown:
        p.set_body(gen_html(p.get_body()))
    return markdown

def get_components():
    return db.session.query(Component).all()


@app.route("/") #декоратор, указывает путь на адрес страницы
@app.route("/index")
def index():
    q = alchemy.select(Post).order_by(Post.date_created.desc())
    posts = db.session.scalars(q).all()
    return render_template("index.html", title = "Home", user = current_user, posts = get_html(posts), components = get_html(get_components()))


@app.route("/posts/<int:id>")
def post(id):
    post = Post.query.get(id)
    post.post_body = gen_html(post.post_body)
    return render_template("post.html", post = post, components = get_html(get_components()))


@app.route("/login", methods = ['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for("index"))
    
    form = LoginForm()
    if form.validate_on_submit():
        user = db.session.scalar(alchemy.select(User).where(User.username == form.username.data))
        if user is None or not user.check_password(form.password.data):
            flash("Invalete Username or password")
            return redirect(url_for("login"))
        login_user(user, remember=form.remember_me)
        return redirect(url_for("index"))
    
    return render_template("login_form.html", form = form, title = "Log in", components = get_html(get_components()))


@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for("index"))


@app.route("/register", methods = ['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for("index"))
    form = Registration()
    if form.validate_on_submit():
        user = User(username = form.username.data, email = form.email.data, question = form.question.data, answer = form.answer.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash(f"Welcome new user!")
        return redirect(url_for("login"))
    return render_template("registration.html", form = form, title = "Register")


@app.route("/admin/<username>")
@login_required
def admin(username):
    posts = db.session.query(Post).all()
    user = db.first_or_404(alchemy.select(User).where(User.username == username))
    components = db.session.query(Component).all()
    return render_template("admin.html", user = user, posts = posts, components = components)


@app.route("/admin/post_editor/<action>", methods = ['GET', 'POST'])
@login_required
def post_editor(action):
    id = request.args.get("id")
    if action == "update" and request.method == "GET":
        post = db.session.query(Post).get(id)
        form = PostEditor()
        form.post_body.data = post.post_body
        return render_template("posteditor.html", form = form, post = post, title = "Post editor", components = get_html(get_components()))
    form = PostEditor()
    
    if form.validate_on_submit():
        title = form.post_title.data
        body = form.post_body.data
        if action == "new":
            new_post = Post(post_title = title, post_body = body, author = current_user)
            db.session.add(new_post)
            db.session.commit()
            flash("Added new post")
        if action == "update":
            post = db.session.query(Post).get(id)
            post.post_title = form.post_title.data
            post.post_body = form.post_body.data
            db.session.commit()
          
        return redirect(url_for("admin", username = current_user.username))
    return render_template("posteditor.html", form = form, title = "Post editor", components = get_html(get_components()))

@app.route("/admin/delete", methods = ['GET', 'POST'])
def delete():
    id = request.args.get("id")
    post = db.session.query(Post).get(id)
    db.session.query(Post).filter_by(id = id).delete()
    db.session.commit()
    return redirect(url_for("admin", username = current_user.username))

@app.route("/admin/component_editor/<action>", methods = ['GET', 'POST'])
def component_editor(action):
    id = request.args.get("id")
    if action == "update" and request.method == "GET":
        component = db.session.query(Component).get(id)
        form = ComponentEditor()
        form.component_body.data = component.component_body
        return render_template("component_editor.html", form = form, component = component, title = "Component editor", components = get_html(get_components()))
    form = ComponentEditor()

    if form.validate_on_submit():
        title = form.component_title.data
        body = form.component_body.data
        component_type = form.component_type.data
        print(component_type)
        if action == "new":
            new_component = Component(component_title = title, component_body = body, component_type = component_type)
            db.session.add(new_component)
            db.session.commit()
            flash("Added new_component")
        if action == "update":
            component = db.session.query(Component).get(id)
            component.component_title = form.component_title.data
            component.component_body = form.component_body.data
            component.component_type = form.component_type.data
            db.session.commit()
        return redirect(url_for("admin", username = current_user.username))          
    return render_template("component_editor.html", form = form, title = "component_editor", components = get_html(get_components()))

@app.route("/admin/component_delete", methods = ['GET', 'POST'])
def component_delete():
    id = request.args.get("id")
    #component = db.session.query(Component).get(id)
    db.session.query(Component).filter_by(id = id).delete()
    db.session.commit()
    return redirect(url_for("admin", username = current_user.username))

@app.route("/password_reset", methods = ['GET', 'POST'])
def password_reset():
    form = PasswordResetForm()
    if form.validate_on_submit():
        username = form.username.data
        user = db.session.query(User).filter_by(username = username).first()
        answer = form.answer.data
        if user.answer == answer:
            user.password_hash = user.set_password(form.password.data)
    return render_template("passwordresetform.html", form = form, title = "password reset form")

@app.route("/start_reset", methods = ['GET', 'POST'])
def start_reset():
    form = GetReset()
    return render_template("getreset.html", form = form, title = "getreset")