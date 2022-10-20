from flask_sqlalchemy import SQLAlchemy
from flask import Flask, render_template, request, flash, redirect, url_for
from flask_login import UserMixin, login_user, LoginManager, login_required, logout_user, current_user
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, EmailField, IntegerField, SubmitField
from wtforms.validators import InputRequired, Length, ValidationError, EqualTo, NumberRange
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///blog.db'
app.config['SECRET_KEY'] = 'cd48ac70-1a42-4060-8148-18fde86bc196'

db = SQLAlchemy(app)

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "login"


@login_manager.user_loader
def load_user(user_id):
    return Users.query.get(int(user_id))


class Users(db.Model, UserMixin):
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


class RegisterForm(FlaskForm):
    email = EmailField(validators=[InputRequired(), Length(min=6, max=20)], render_kw={"placeholder": "email"})
    name = StringField(validators=[InputRequired(), Length(min=6, max=20)], render_kw={"placeholder": "имя"})
    age = IntegerField(validators=[InputRequired(), NumberRange(min=0, max=100)], render_kw={"placeholder": "возраст"})
    city = StringField(validators=[InputRequired(), Length(min=6, max=20)], render_kw={"placeholder": "город"})
    password = PasswordField(validators=[InputRequired(), Length(min=6, max=20),
                                         EqualTo('confirm', message='Пароли должны совпадать')],
                             render_kw={"placeholder": "пароль"})
    confirm = PasswordField(validators=[InputRequired(), Length(min=6, max=20)], render_kw={"placeholder": "Повтори пароль"})

    submit = SubmitField("Регистрация")

    def validate_email(self, email):
        existing_user_email = Users.query.filter_by(email=email.data).first()

        if existing_user_email:
            flash("Пользователь с такой почтой уже зарегистрирован. :(", category="danger")
            raise ValidationError("Пользователь с такой почтой уже зарегистрирован. Выбери другую почту.")


class LoginForm(FlaskForm):
    email = EmailField(validators=[InputRequired(), Length(min=6, max=20)], render_kw={"placeholder": "email"})
    password = PasswordField(validators=[InputRequired(), Length(min=6, max=20)], render_kw={"placeholder": "пароль"})

    submit = SubmitField("Войти")


menu = [
    {"name": "Блог", "url": "/"},
    {"name": "Подкаст", "url": "/podcast"},
    {"name": "Сообщество", "url": "/community"},
    {"name": "Дашборд", "url": "/dashboard"},
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
    form = LoginForm()

    if form.validate_on_submit():
        user = Users.query.filter_by(email=form.email.data).first()
        if user:
            if check_password_hash(user.password, form.password.data):
                login_user(user)
                return redirect(url_for('dashboard'))

    return render_template('login.html', menu=menu, title="Авторизация", form=form)


@app.route("/dashboard", methods=["POST", "GET"])
@login_required
def dashboard():
    user = Users.query.get(current_user.get_id())
    return render_template('dashboard.html', menu=menu, title="Дашборд", user=user)


@app.route("/logout", methods=["POST", "GET"])
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))


@app.route("/register", methods=["POST", "GET"])
def register():
    form = RegisterForm()

    if form.validate_on_submit():
        try:
            hash = generate_password_hash(form.password.data)
            u = Users(
                email=form.email.data,
                password=hash
            )
            db.session.add(u)
            db.session.flush()

            p = Profiles(
                name=form.name.data,
                age=form.age.data,
                city=form.city.data,
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

    return render_template('register.html', menu=menu, title="Регистрация", form=form)


if __name__ == "__main__":
    app.run(debug=True)
