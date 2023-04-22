import sqlalchemy as sa
from flask_login import UserMixin

from . import db


class User(UserMixin, db.Model):
    id = sa.Column(sa.Integer, primary_key=True)
    login = sa.Column(sa.String(20), unique=True)
    email = sa.Column(sa.String(100), unique=True)
    pass_hash = sa.Column(sa.String(100))
    pass_salt = sa.Column(sa.String(100))
