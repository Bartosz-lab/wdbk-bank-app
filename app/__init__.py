from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_apscheduler import APScheduler

# init SQLAlchemy so we can use it later in our models
db = SQLAlchemy()
scheduler = APScheduler()


def create_app():
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_object("config")
    app.config.from_pyfile("config.py", silent=True)

    login_manager = LoginManager()
    login_manager.login_view = "auth.login"
    login_manager.init_app(app)

    from . import models

    @login_manager.user_loader
    def load_user(user_id):
        # since the user_id is just the primary key of our user table, use it in the query for the user
        return models.User.query.get(int(user_id))

    from .auth import auth as auth_blueprint
    from .main import main as main_blueprint
    from .transfer import transfer as transfer_blueprint

    app.register_blueprint(auth_blueprint)
    app.register_blueprint(main_blueprint)
    app.register_blueprint(transfer_blueprint)

    db.init_app(app)
    with app.app_context():
        db.create_all()

    scheduler.init_app(app)
    scheduler.start()

    return app
