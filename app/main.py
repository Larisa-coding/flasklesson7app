from flask import Flask, render_template, request, redirect, url_for, flash, session
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.secret_key = "supersecretkey"

users = {
    "user1": {
        "name": "Иван Иванов",
        "email": "ivan@example.com",
        "password": generate_password_hash("password123")
    }
}

@app.route("/")
def home():
    if "username" in session:
        return redirect(url_for("profile"))
    return redirect(url_for("login"))

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")

        if username in users and check_password_hash(users[username]["password"], password):
            session["username"] = username
            flash("Вы успешно вошли в систему!", "success")
            return redirect(url_for("profile"))
        else:
            flash("Неверное имя пользователя или пароль", "error")

    return render_template("login.html")

@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        username = request.form.get("username")
        name = request.form.get("name")
        email = request.form.get("email")
        password = request.form.get("password")

        if username in users:
            flash("Пользователь с таким именем уже существует", "error")
        else:
            users[username] = {
                "name": name,
                "email": email,
                "password": generate_password_hash(password)
            }
            flash("Регистрация прошла успешно! Теперь вы можете войти.", "success")
            return redirect(url_for("login"))

    return render_template("register.html")

@app.route("/profile", methods=["GET", "POST"])
def profile():
    if "username" not in session:
        flash("Пожалуйста, войдите в систему", "error")
        return redirect(url_for("login"))

    username = session["username"]
    user = users[username]

    if request.method == "POST":
        user["name"] = request.form.get("name")
        user["email"] = request.form.get("email")
        new_password = request.form.get("new_password")

        if new_password:
            user["password"] = generate_password_hash(new_password)

        flash("Профиль успешно обновлен!", "success")
        return redirect(url_for("profile"))

    return render_template("profile.html", user=user)

@app.route("/logout")
def logout():
    session.pop("username", None)
    flash("Вы успешно вышли из системы", "success")
    return redirect(url_for("login"))

if __name__ == "__main__":
    app.run(debug=True)