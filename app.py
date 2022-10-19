from flask_sqlalchemy import SQLAlchemy
from flask import Flask, render_template, request, flash, redirect, url_for
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///blog.db'
app.config['SECRET_KEY'] = 'cd48ac70-1a42-4060-8148-18fde86bc196'

db = SQLAlchemy(app)


class Users(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(50), unique=True)
    password = db.Column(db.String(500), nullable=True)
    date = db.Column(db.DateTime, default=datetime.utcnow)

    pr = db.relationship('Profiles', backref='users', uselist=False)

    def __repr__(self):
        return f"<users {self.id}"


class Profiles(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), unique=True)
    age = db.Column(db.Integer)
    city = db.Column(db.String(50))

    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))

    def __repr__(self):
        return f"<users {self.id}"


menu = [
    {"name": "Блог", "url": "/"},
    {"name": "Подкаст", "url": "/podcast"},
    {"name": "Сообщество", "url": "/community"},
    {"name": "Войти", "url": "/login"},
]


@app.route("/")
def index():
    return render_template("index.html", menu=menu, title="Блог")


@app.route("/podcast")
def podcast():
    return render_template('podcast.html', menu=menu, title="Подкаст")


@app.route("/community")
def community():
    return render_template('community.html', menu=menu, title="Сообщество")


@app.errorhandler(404)
def page_not_found(error):
    return render_template('page404.html', menu=menu, title="Ошибка 404"), 404


@app.route("/login", methods=["POST", "GET"])
def login():

    if request.method == "POST":
        f = Users.query.filter_by(email = request.form['email']).first()

        if not f:
            flash("Участник с таким email не зарегистрирован.", category="danger")

        password = Users.query.get(f.id).password
        if not check_password_hash(password, request.form['password']):
            flash("Неверный пароль.", category="danger")
        else:
            return redirect(url_for('index'))

    return render_template('login.html', menu=menu, title="Авторизация")


@app.route("/register", methods=["POST", "GET"])
def register():

    if request.method == "POST":
        if not (len(request.form['email']) > 8 and len(request.form['name']) > 3 and len(request.form['password']) > 5
                and request.form['password'] == request.form['password_repeat']):
            flash("Некорректные данные :(", category="danger")
        else:
            try:
                hash = generate_password_hash(request.form['password'])
                u = Users(
                    email=request.form['email'],
                    password=hash
                )
                db.session.add(u)
                db.session.flush()

                p = Profiles(
                    name=request.form['name'],
                    age=request.form['age'],
                    city=request.form['city'],
                    user_id=u.id
                )
                db.session.add(p)
                db.session.commit()
            except:
                db.session.rollback()
                print("Ошибка добавления в базу данных")
                flash("Некорректные данные :(", category="danger")
            else:
                flash("Регистрация прошла успешно :)", category="success")

    return render_template('register.html', menu=menu, title="Регистрация")


if __name__ == "__main__":
    app.run(debug=True)
