"""
Задание

Создать страницу, на которой будет форма для ввода имени и электронной почты, при отправке которой будет создан
cookie-файл с данными пользователя, а также будет произведено перенаправление на страницу приветствия, где будет
отображаться имя пользователя.
На странице приветствия должна быть кнопка «Выйти», при нажатии на которую будет удалён cookie-файл с данными
пользователя и произведено перенаправление на страницу ввода имени и электронной почты.
"""

from flask import (
    Flask,
    render_template,
    redirect,
    make_response,
    request,
    session,
    url_for,
)


app = Flask(__name__)
app.secret_key = "secret_key"


@app.route("/", methods=["GET", "POST"])
def index():
    """
    Страница с формой ввода
    пользовательских данных
    """
    if request.method == "POST":                             # Если метод запроса POST
        response = make_response("Cookies")
        username = request.form.get("username")              # Получаем username и email  из формы
        user_email = request.form.get("email")
        if len(user_email) != 0 and len(username) != 0:           # Проверка введены ли данные
            response.set_cookie("username", value="username", max_age=None)
            response.set_cookie("email", value="email", max_age=None)  # Создаем cookie почты и username
            session["usename"] = username
            session["email"] = user_email                                # Создаем сессию пользователя с email и username
            return redirect(url_for("user", username=username))
        return redirect(url_for("index"))                           # переход на страницу пользователя
    return render_template("index.html")

@app.route("/user/<string:username>/", methods=["GET", "POST"])
def user(username, *args, **kwargs):
    """
    Старница приветствия ползователя
    """
    if session:                             # Проверка наличия сесии
        if request.method == "POST":                          # Если метод Post (кнопка выход)
            response = make_response("Cookie clear")
            if request.cookies.get("sessionid") and request.cookies.get("session"):   # Проверяем наличие cookie сессии
                response.set_cookie("csrftoken", "", expires=0)
                response.set_cookie("sessionid", "", expires=0)         # Очищаем cookie сесиии
                response.set_cookie("session",'',expires=0)
                print('Cookie удалены')
                session.clear()                                   # Удалаяем сессию
                return redirect(url_for("index"))               # Возвращаемся на стартовую страницу
            print(request.cookies)
            print(response)
            print("Не удалось очистить Cookie")
            return redirect(url_for("index"))
        return render_template("user.html", username=username)
    return redirect(url_for("index"))


if __name__ == "__main__":
    app.run(debug=True)