from flask import Flask, render_template, request, redirect, session, url_for, flash
from database import init_db, create_user, find_user_insecure

app = Flask(__name__)

# ❌ Intentionally weak secret key (we'll fix later)
app.secret_key = "devkey"


@app.before_request
def _init():
    # Safe to call repeatedly; table creation uses IF NOT EXISTS
    init_db()


@app.route("/")
def index():
    user = session.get("user")
    role = session.get("role")
    return render_template("index.html", user=user, role=role)


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "GET":
        return render_template("login.html")

    username = request.form.get("username", "")
    password = request.form.get("password", "")

    row = find_user_insecure(username, password)
    if row:
        session["user"] = row["username"]
        session["role"] = row["role"]
        return redirect(url_for("index"))

    flash("Invalid username or password.")
    return redirect(url_for("login"))


@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "GET":
        return render_template("register.html")

    username = request.form.get("username", "").strip()
    password = request.form.get("password", "")

    if not username or not password:
        flash("Username and password required.")
        return redirect(url_for("register"))

    # ❌ Plaintext password storage (intentional)
    ok = create_user(username, password, role="user")
    if not ok:
        flash("Username already taken.")
        return redirect(url_for("register"))

    flash("Account created. Please log in.")
    return redirect(url_for("login"))


@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("index"))


if __name__ == "__main__":
    # ❌ debug=True is intentionally unsafe (we'll fix later)
    app.run(debug=True)
