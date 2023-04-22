import sqlalchemy as sa
from flask_login import UserMixin
from flask_scrypt import (
    generate_random_salt,
    generate_password_hash,
    check_password_hash,
)

from . import db


class User(UserMixin, db.Model):
    id = sa.Column(sa.Integer, primary_key=True)
    login = sa.Column(sa.String(20), unique=True)
    email = sa.Column(sa.String(100), unique=True)
    pass_hash = sa.Column(sa.String(100))
    pass_salt = sa.Column(sa.String(100))

    def __init__(self, login, email, password) -> None:
        self.login = login
        self.email = email

        self.change_password(password)

        return self

    def check_password(self, password):
        return check_password_hash(password, self.pass_hash, self.pass_salt)

    def change_password(self, password):
        self.pass_salt = generate_random_salt()
        self.pass_hash = generate_password_hash(password, self.pass_salt)


class Transfer(db.Model):
    id = sa.Column(sa.Integer, primary_key=True)
    title = sa.Column(sa.String(50), nullable=False)
    date = sa.Column(sa.Date(), nullable=False)
    amount = sa.Column(sa.Numeric(scale=2), nullable=False)
    iban = sa.Column(sa.String(40))
    user_id = sa.Column(sa.Integer, sa.ForeignKey(User.id), nullable=False)
