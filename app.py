from flask import Flask, render_template, request, redirect, url_for, session, flash
from system.friend_manager import FriendManager
from system.recommendation_engine import recommend_friends

app = Flask(__name__)
app.secret_key = "eplace-this-with-a-secure-key"
fm = FriendManager()


def get_current_user():
    return session.get("username")


@app.route("/")
def index():
    if not get_current_user():
        return redirect(url_for("login"))
    return redirect(url_for("network"))


@app.route("/login", methods=["GET", "POST"])
def login():
    if get_current_user():
        return redirect(url_for("network"))

    if request.method == "POST":
        username = request.form.get("username", "").strip()
        password = request.form.get("password", "").strip()

        if fm.login(username, password):
            session["username"] = username
            flash("Login successful.", "success")
            return redirect(url_for("network"))

        flash("Invalid username or password.", "danger")

    return render_template("login.html")


@app.route("/register", methods=["GET", "POST"])
def register():
    if get_current_user():
        return redirect(url_for("network"))

    if request.method == "POST":
        username = request.form.get("username", "").strip()
        password = request.form.get("password", "").strip()

        if not username or not password:
            flash("Username and password are required.", "danger")
        elif fm.create_user(username, password):
            flash("Registration complete. Please log in.", "success")
            return redirect(url_for("login"))
        else:
            flash("Username already exists.", "danger")

    return render_template("register.html")


@app.route("/logout")
def logout():
    session.pop("username", None)
    flash("Logged out.", "info")
    return redirect(url_for("login"))


@app.route("/network")
def network():
    user = get_current_user()
    if not user:
        return redirect(url_for("login"))

    return render_template(
        "network.html",
        user=user,
        network=fm.network,
    )


@app.route("/send-request", methods=["POST"])
def send_request():
    user = get_current_user()
    if not user:
        return redirect(url_for("login"))

    receiver = request.form.get("receiver", "").strip()
    if not receiver:
        flash("Receiver username is required.", "danger")
    elif receiver == user:
        flash("You cannot send a request to yourself.", "danger")
    elif receiver not in fm.network:
        flash("Receiver does not exist.", "danger")
    else:
        fm.send_request(user, receiver)
        flash(f"Friend request sent to {receiver}.", "success")

    return redirect(url_for("network"))


@app.route("/accept-request", methods=["POST"])
def accept_request():
    user = get_current_user()
    if not user:
        return redirect(url_for("login"))

    sender = request.form.get("sender", "").strip()
    if not sender:
        flash("Sender username is required.", "danger")
    elif sender not in fm.network:
        flash("Sender does not exist.", "danger")
    elif sender == user:
        flash("Invalid sender.", "danger")
    else:
        fm.accept_request(sender, user)
        flash(f"Friend request accepted from {sender}.", "success")

    return redirect(url_for("network"))


@app.route("/recommendations")
def recommendations():
    user = get_current_user()
    if not user:
        return redirect(url_for("login"))

    recs = recommend_friends(fm.network, user)
    return render_template("recommendations.html", user=user, recommendations=recs)


@app.route("/undo", methods=["POST"])
def undo():
    user = get_current_user()
    if not user:
        return redirect(url_for("login"))

    fm.undo()
    flash("Undo completed.", "info")
    return redirect(url_for("network"))


@app.route("/delete-user", methods=["POST"])
def delete_user():
    user = get_current_user()
    if not user:
        return redirect(url_for("login"))

    username = request.form.get("username", "").strip()
    if not username:
        flash("Username is required.", "danger")
    elif username not in fm.network:
        flash("User does not exist.", "danger")
    else:
        fm.delete_user(username)
        flash(f"User {username} deleted.", "success")
        if username == user:
            session.pop("username", None)
            return redirect(url_for("login"))

    return redirect(url_for("network"))


if __name__ == "__main__":
    app.run(debug=True)
