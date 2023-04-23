import os

basedir = os.path.abspath(os.path.dirname(__file__))


class Config(object):
    SECRET_KEY = os.getenv("SECRET_KEY", "secret-key-goes-here")
    SQLALCHEMY_DATABASE_URI = os.getenv("DATABASE_URL", "sqlite://")
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_ECHO = False
    MAIL_SERVER = os.getenv("MAIL_SERVER", "placeholder.local")
    MAIL_PORT = os.getenv("MAIL_PORT", 587)
    MAIL_USE_TLS = os.getenv("MAIL_USE_TLS", True)
    MAIL_USERNAME = os.getenv("MAIL_USERNAME", "user")
    MAIL_PASSWORD = os.getenv("MAIL_PASSWORD", "pass")
    MAIL_DEFAULT_SENDER = os.getenv("MAIL_DEFAULT_SENDER", "user@placeholder.local")
