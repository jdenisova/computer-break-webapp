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


if __name__ == "__main__":
    app.run(debug=True)
