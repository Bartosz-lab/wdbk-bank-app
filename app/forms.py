from flask import url_for
from flask_wtf import FlaskForm
from wtforms import StringField, EmailField, PasswordField
from wtforms import validators as va
from password_strength import PasswordPolicy

from .models import User

policy = PasswordPolicy.from_names(
    length=8,  # min length: 8
    uppercase=1,  # need min. 2 uppercase letters
    numbers=1,  # need min. 2 digits
    special=1,  # need min. 2 special characters
    nonletters=2,  # need min. 2 non-letter characters (digits, specials, anything)
)


class SignUpForm(FlaskForm):
    login = StringField(
        "Login", validators=[va.InputRequired(), va.Length(min=5, max=25)]
    )
    email = EmailField("Email", validators=[va.InputRequired(), va.Email()])
    password = PasswordField(
        "Password",
        validators=[
            va.InputRequired(),
        ],
    )
    confirm = PasswordField(
        "Repeat Password",
        validators=[
            va.InputRequired(),
            va.EqualTo("password", message="Passwords must match"),
        ],
    )

    def validate_password(form, field):
        if policy.test(field.data) != []:
            raise va.ValidationError("Password is to week")

    def validate_login(form, field):
        if form.login.errors:
            raise va.StopValidation()
        # if this returns a user, then the login already exists in database
        user = User.query.filter_by(login=field.data).first()
        print("UPS", field.data)
        if user:
            raise va.ValidationError(f"Login already exists")
