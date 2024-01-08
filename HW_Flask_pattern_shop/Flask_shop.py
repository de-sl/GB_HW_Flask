from flask import Flask
from flask import render_template

app = Flask(__name__)
@app.route('/')
def basic_index():
    context = {"title": "Главная"}
    return render_template("basic_index.html")
@app.route('/cloth/')
def op_cloth():
    context = {"title": "Одежда"}
    return render_template("cloth.html")

@app.route('/shoes/')
def op_shoes():
    context = {"title": "Обувь"}
    return render_template("shoes.html")

@app.route('/jacket/')
def op_jacket():
    context = {"title": "Куртки"}
    return render_template("jacket.html")

if __name__ == '__main__':
    app.run(debug=True)

