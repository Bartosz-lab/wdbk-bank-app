from flask import Blueprint, render_template, redirect, url_for, request, flash
from flask_login import login_user, login_required, logout_user
from flask_scrypt import (
    generate_random_salt,
    generate_password_hash,
    check_password_hash,
)

from .models import User
from . import db

auth = Blueprint("auth", __name__)


@auth.get("/login")
def login():
    return render_template("login.html")


@auth.post("/login")
def login_post():
    login = request.form.get("login")
    password = request.form.get("password")
    remember = True if request.form.get("remember") else False

    user: User = User.query.filter_by(login=login).first()
    print(user)
    print(login)

    # check if the user actually exists
    # take the user-supplied password, hash it, and compare it to the hashed password in the database
    if not user or not check_password_hash(password, user.pass_hash, user.pass_salt):
        flash("Please check your login details and try again.")
        return redirect(
            url_for("auth.login")
        )  # if the user doesn't exist or password is wrong, reload the page

    # if the above check passes, then we know the user has the right credentials
    login_user(user, remember=remember)
    return redirect(url_for("main.profile"))


@auth.get("/signup")
def signup():
    return render_template("signup.html")


@auth.post("/signup")
def signup_post():
    login = request.form.get("login")
    email = request.form.get("email")
    password = request.form.get("password")

    # if this returns a user, then the login already exists in database
    user = User.query.filter_by(login=login).first()

    if user:
        # if a user is found, we want to redirect back to signup page so user can try again
        flash("Login already exists")
        return redirect(url_for("auth.signup"))

    pass_salt = generate_random_salt()
    pass_hash = generate_password_hash(password, pass_salt)
    new_user = User(email=email, login=login, pass_hash=pass_hash, pass_salt=pass_salt)

    # add the new user to the database
    db.session.add(new_user)
    db.session.commit()

    return redirect(url_for("auth.login"))


@auth.get("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for("main.index"))
