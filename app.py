from flask import Flask, render_template, request, redirect, session, url_for, flash
from database import (
    init_db,
    ensure_admin_seed,
    create_user,
    find_user_insecure,
    create_note,
    get_notes_for_user,
    get_all_users_and_note_counts,
    get_user_id_by_username,
)

app = Flask(__name__)
app.secret_key = "devkey"  # intentionally weak


@app.before_request
def _setup():
    init_db()
    ensure_admin_seed()  # creates admin/adminpass if missing


def require_login():
    if "user" not in session:
        flash("Please log in first.")
        return False
    return True


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

    ok = create_user(username, password, role="user")  # plaintext passwords
    if not ok:
        flash("Username already taken.")
        return redirect(url_for("register"))

    flash("Account created. Please log in.")
    return redirect(url_for("login"))


@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("index"))


@app.route("/notes", methods=["GET", "POST"])
def notes():
    if not require_login():
        return redirect(url_for("login"))

    username = session["user"]
    user_id = get_user_id_by_username(username)
    if user_id is None:
        session.clear()
        flash("Session user not found. Please log in again.")
        return redirect(url_for("login"))

    if request.method == "POST":
        content = request.form.get("content", "")
        if content.strip():
            create_note(user_id, content)  # will enable XSS testing later
        return redirect(url_for("notes"))

    rows = get_notes_for_user(user_id)
    return render_template("notes.html", user=username, notes=rows)


@app.route("/admin")
def admin():
    # INTENTIONALLY BROKEN ACCESS CONTROL:
    # Anyone who is logged in (or even not logged in) can view admin data.
    users = get_all_users_and_note_counts()
    return render_template("admin.html", users=users)

@app.route("/xss-collect")
def xss_collect():
    """
    Intentionally insecure endpoint used to demonstrate XSS data exfiltration.
    """
    payload = request.args.get("d", "")
    print(f"[XSS-COLLECT] Received: {payload}")
    return "ok"



if __name__ == "__main__":
    app.run(debug=True)  # intentionally unsafe
