import logging
import os

from flask import Flask, render_template, request, redirect, session, url_for, flash
from config import Config
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
app.config.from_object(Config)

# ---- Logging Setup ----
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(levelname)s %(message)s"
)


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
    if "user" not in session:
        logging.warning("Unauthorized admin access attempt (not logged in) from %s", request.remote_addr)
        flash("Admin access required.")
    if session.get("role") != "admin":
        logging.warning("Unauthorized admin access attempt by user=%s from %s", session.get("user"), request.remote_addr)
        flash("Admin access required.")
        return False
    return True


@app.after_request
def add_security_headers(resp):
    # Defense-in-depth headers.
    resp.headers["X-Content-Type-Options"] = "nosniff"
    resp.headers["X-Frame-Options"] = "DENY"
    resp.headers["Referrer-Policy"] = "no-referrer"
    resp.headers["Content-Security-Policy"] = "default-src 'self'; object-src 'none'; bse-uri 'self'; frame-ancestors 'none'"

    return resp


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
        logging.info("Login success user=%s ip=%s", user["username"], request.remote_addr)
        return redirect(url_for("index"))

    logging.warning("Login failed username=%s ip=%s", username, request.remote_addr)
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

    logging.info("User registered username=%s ip=%s", username, request.remote_addr)
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
            logging.info("Note created user=%s ip=%s", session.get("user"), request.remote_addr)
        return redirect(url_for("notes"))

    notes = get_notes_for_user(user_id)
    return render_template("notes.html", user=session["user"], notes=notes)


@app.route("/admin")
def admin():
    if not require_admin():
        return redirect(url_for("index"))

    users = get_all_users_and_note_counts()
    logging.info("Admin page viewed by user=%s ip=%s", session.get("user"), request.remote_addr)
    return render_template("admin.html", users=users)


@app.route("/logout")
def logout():
    logging.info("Logout user=%s ip=%s", session.get("user"), request.remote_addr)
    session.clear()
    return redirect(url_for("index"))


if __name__ == "__main__":
    debug = os.environ.get("FLASK_DEBUG") == "1"
    app.run(debug=debug)
