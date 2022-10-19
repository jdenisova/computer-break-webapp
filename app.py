from flask import Flask, render_template

app = Flask(__name__)


menu = [
    {"name": "Блог", "url": "/"},
    {"name": "Подкаст", "url": "/podcast"},
    {"name": "Сообщество", "url": "/community"},
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


if __name__ == "__main__":
    app.run(debug=True)
