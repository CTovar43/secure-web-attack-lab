from flask import Flask, render_template, request, redirect, session, url_for, flash
from database import (
    init_db,
    ensure_admin_seed,
    create_user,
    find_user_secure,
    create_note,
    get_notes_for_user,
    get_all_users_and_note_counts,
    get_user_id_by_username,
)

app = Flask(__name__)
app.secret_key = "devkey"  # will harden later


@app.before_request
def setup():
    init_db()
    ensure_admin_seed()


def require_login():
    if "user" not in session:
        flash("Please log in first.")
        return False
    return True


def require_admin():
    if "user" not in session or session.get("role") != "admin":
        flash("Admin access required.")
        return False
    return True


@app.route("/")
def index():
    return render_template(
        "index.html",
        user=session.get("user"),
        role=session.get("role"),
    )


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "GET":
        return render_template("login.html")

    username = request.form.get("username", "")
    password = request.form.get("password", "")

    user = find_user_secure(username, password)
    if user:
        session["user"] = user["username"]
        session["role"] = user["role"]
        return redirect(url_for("index"))

    flash("Invalid credentials.")
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

    if not create_user(username, password):
        flash("Username already exists.")
        return redirect(url_for("register"))

    flash("Account created. Please log in.")
    return redirect(url_for("login"))


@app.route("/notes", methods=["GET", "POST"])
def notes():
    if not require_login():
        return redirect(url_for("login"))

    user_id = get_user_id_by_username(session["user"])

    if request.method == "POST":
        content = request.form.get("content", "")
        if content.strip():
            create_note(user_id, content)
        return redirect(url_for("notes"))

    notes = get_notes_for_user(user_id)
    return render_template("notes.html", user=session["user"], notes=notes)


@app.route("/admin")
def admin():
    if not require_admin():
        return redirect(url_for("index"))

    users = get_all_users_and_note_counts()
    return render_template("admin.html", users=users)


@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("index"))


if __name__ == "__main__":
    app.run(debug=True)
