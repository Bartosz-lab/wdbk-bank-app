from flask import Blueprint, render_template, redirect, url_for, request, flash
from flask_login import login_user, login_required, logout_user, current_user


from .models import User
from .forms import SignUpForm, ChangePassForm, ResetPassForm
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

    # check if the user actually exists
    # take the user-supplied password, hash it, and compare it to the hashed password in the database
    if not user or not user.check_password(password):
        flash("Please check your login details and try again.")
        return redirect(
            url_for("auth.login")
        )  # if the user doesn't exist or password is wrong, reload the page

    # if the above check passes, then we know the user has the right credentials
    login_user(user, remember=remember)
    return redirect(url_for("main.profile"))


@auth.route("/signup", methods=("GET", "POST"))
def signup():
    form = SignUpForm()
    if form.validate_on_submit():
        new_user = User(
            email=form.email.data, login=form.login.data, password=form.password.data
        )

        # add the new user to the database
        db.session.add(new_user)
        db.session.commit()

        return redirect(url_for("auth.login"))

    return render_template("signup.html", form=form)


@auth.get("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for("main.index"))


@auth.route("/changepass", methods=("GET", "POST"))
@login_required
def changepass():
    form = ChangePassForm()
    if form.validate_on_submit():
        current_user.change_password(form.password.data)

        db.session.commit()

    return render_template(
        "changepass.html", form=form, login=current_user.login, email=current_user.email
    )


@auth.route("/resetpass", methods=("GET", "POST"))
def resetpass():
    form = ResetPassForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user:
            user.change_password("pass")
            db.session.commit()

        flash(
            "If user exists password has been sent to your mail. Joke, your password now is 'pass'",
            "warning",
        )
        return redirect(
            url_for("auth.login")
        )  # if the user doesn't exist or password is wrong, reload the page
    return render_template("resetpass.html", form=form)
