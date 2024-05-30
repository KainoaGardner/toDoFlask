from app import app, db
from flask import redirect, render_template, url_for, request, session, flash
from app.forms import User, ToDoList


@app.route("/")
@app.route("/home")
def home():
    return render_template("home.html")


@app.route("/admin", methods=["GET", "POST"])
def admin():
    if "username" not in session or session["username"] != "Admin":
        return redirect(url_for("home"))

    if request.method == "POST":
        username = request.form["remove_username"]
        foundUser = User.query.filter_by(name=username).first()
        if foundUser:
            db.session.delete(foundUser)
            db.session.commit()

    users = User.query.all()
    return render_template("admin.html", users=users)


@app.route("/user", methods=["GET", "POST"])
def user():
    if "username" not in session:
        return redirect("login")

    username = session["username"]
    entries = []
    foundUser = User.query.filter_by(name=username).first()
    entries = foundUser.toDo

    if request.method == "POST":
        if "entry" in request.form:
            text = request.form["entry"]
            if text:
                entry = ToDoList(text)

                foundUser.toDo.append(entry)
                db.session.add(entry)
                db.session.commit()

    return render_template("user.html", username=username, entries=entries)


@app.route("/remove/<id>")
def remove(id):
    foundUser = ToDoList.query.filter_by(id=id).delete()
    db.session.commit()
    return redirect(url_for("user"))


@app.route("/complete/<id>")
def complete(id):
    foundUser = ToDoList.query.filter_by(id=id).first()
    foundUser.complete = True
    db.session.commit()
    return redirect(url_for("user"))


@app.route("/uncomplete/<id>")
def uncomplete(id):
    foundUser = ToDoList.query.filter_by(id=id).first()
    foundUser.complete = False
    db.session.commit()
    return redirect(url_for("user"))


@app.route("/login", methods=["GET", "POST"])
def login():
    session.permanent = True
    if "username" in session:
        return redirect(url_for("user"))

    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        foundUser = User.query.filter_by(name=username).first()
        if foundUser and foundUser.password == password:
            session["username"] = username
            return redirect(url_for("user"))

    return render_template("login.html")


@app.route("/logout")
def logout():
    session.pop("username", None)
    return redirect(url_for("login"))


@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        foundUser = User.query.filter_by(name=username).first()
        if foundUser:
            return redirect(url_for("register"))
        else:
            user = User(username, password)
            db.session.add(user)
            db.session.commit()

            return redirect(url_for("login"))
    return render_template("register.html")
