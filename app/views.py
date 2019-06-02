from app import app

from flask import render_template, jsonify, session, redirect

import app.models   as models
import pymysql      as sql
from flask import request

@app.route("/", methods = ["GET"])
def route_index():
    if (session.get("username")):
        return redirect("/user/task")
    return render_template(
        "index.html",
        title = "EpiTodo",
        content = "Hello, world!"
    )

@app.route("/register", methods = ["GET", "POST"])
def route_register():
    if (session.get("username")):
        return redirect("/user/task")
    username = request.form.get('username')
    password = request.form.get('password')
    if (username and password):
        print("New user: {}".format(username))
        if (models.register_user(username, password)):
            session["username"] = username
            return redirect("/user/task")
    return render_template(
        "register.html"
    )

@app.route("/signin", methods = ["GET", "POST"])
def route_signin():
    if (session.get("username")):
        return redirect("/user/task")
    print("Session username is {}".format(session.get("username")))
    username = request.form.get('username')
    password = request.form.get('password')
    if (username and password):
        print("Auth attempt: {}".format(username))
        if (models.check_user(username, password)):
            session["username"] = username
            print("Success")
            return redirect("/user/task")
        else:
            print("Fail")
    return render_template(
        "signin.html"
    )

@app.route("/user/task", methods = ["GET"])
def route_user_task():
    username = session.get("username")
    if (not username): return redirect("/")
    return render_template(
        "task.html",
        username = username
    )

@app.route("/signout", methods = ["GET"])
def route_signout():
    if (session.get("username")):
        del session["username"]
    return redirect("/")

@app.route("/user")
def route_user():
    models.get_user("user_id", 1)
    return ""
