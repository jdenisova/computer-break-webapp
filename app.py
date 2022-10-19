from flask_sqlalchemy import SQLAlchemy
from flask import Flask, render_template
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///blog.db'

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

    return render_template('login.html', menu=menu, title="Авторизация")


@app.route("/register", methods=["POST", "GET"])
def register():

    return render_template('register.html', menu=menu, title="Регистрация")


if __name__ == "__main__":
    app.run(debug=True)
