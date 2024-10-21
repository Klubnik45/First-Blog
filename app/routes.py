from flask import render_template, flash, redirect, url_for # импорт функций из пакета flask (render_template - принимает имя шаблона и список переменных аргументов шаблона и возвращает готовый шаблон с заменёнными аргументами, flash — используется для отображения временных сообщений пользователю после выполнения определённого запроса, redirect — позволяет перенаправлять пользователей на указанный URL и присваивать указанному коду состояния, url_for - генерация URL)
from app import app, db # импорт переменных
from app.forms import LoginForm, Registration, PostEditor # импорт классов (LoginForm - реализует представление окна входа в систему, Registration - сохранение ссылки на объект одного класса в другом, PostEditor - редактирует сообщения)
from flask_login import current_user, login_user, logout_user, login_required # Flask-Login — это расширение Flask, которое управляет состоянием входа пользователя в систему.
from app.models import User, Post
import sqlalchemy as alchemy

user = {"username": "Alex"}
posts = [{"id":1, "images":['Dragonheart-1.jpg', 'smaug_dragon-1.webp', 'toothless.jpg'], "author": {"username": "Bobby"}, "post_title": "Here There Be Dragons", "post_body": "I trust you all caught “The Red Dragon and the Gold,” the fourth episode of season 2 of HOUSE OF THE DRAGON.   A lot of you have been wanting for action, I know; this episode delivered it in spades with the Battle of Rook’s Rest, when dragon met dragon in the skies."}, {"id":2, "images":[], "author": {"username": user["username"]}, "post_title": "A Bold New Look for the A Song of Ice and Fire Boxed Set", "post_body": "Behold, the stunning new covers for the first five books! These covers will be available in a boxed set, available online and in stores this October."}, {"id":3, "images":[], "author": {"username": "Bobby"}, "post_title": "On the Road Again", "post_body": "We will be headed across the Atlantic in a week or so for the longest trip we’ve taken in a while, part business and part pleasure."}]

@app.route("/") #декоратор, указывает путь на адрес страницы
@app.route("/index")
def index():
    return render_template("index.html", title = "Home", user = user, posts = posts)


@app.route("/posts/<int:id>")
def post(id):
    post = {}
    for p in posts:
        if p["id"] == id:
            post = p
            break
    return render_template("post.html", post = post)


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
    
    return render_template("login_form.html", form = form, title = "Log in")


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
        user = User(username = form.username.data, email = form.email.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash(f"Welcome new user!")
        return redirect(url_for("login"))
    return render_template("registration.html", form = form, title = "Register")


@app.route("/admin/<username>")
@login_required
def admin(username):
    user = db.first_or_404(alchemy.select(User).where(User.username == username))
    return render_template("admin.html", user = user, posts = posts)


@app.route("/admin/post_editor", methods = ['GET', 'POST'])
@login_required
def post_editor():
    form = PostEditor()
    if form.validate_on_submit():
        title = form.post_title.date
        body = form.post_body.date
    return render_template("posteditor.html", form = form, title = "Post editor")