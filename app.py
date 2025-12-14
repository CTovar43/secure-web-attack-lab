from flask import Flask, render_template, request, redirect, session, url_for

app = Flask(__name__)

# ❌ Intentionally weak secret key (will fix later)
app.secret_key = "devkey"


@app.route("/")
def index():
    user = session.get("user")
    return render_template("index.html", user=user)


@app.route("/login", methods=["POST"])
def login():
    username = request.form.get("username")
    password = request.form.get("password")

    # ❌ Authentication logic will be added later (insecure first)
    if username and password:
        session["user"] = username
        return redirect(url_for("index"))

    return redirect(url_for("index"))


@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("index"))


if __name__ == "__main__":
    app.run(debug=True)
