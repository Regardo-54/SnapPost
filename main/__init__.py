from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
import os
from dotenv import load_dotenv
from main.confiq import Confiq

load_dotenv()


db = SQLAlchemy()
login_manager = LoginManager()
login_manager.login_view = 'users.login'
login_manager.login_message_category = 'info'


def create_app(confiq_class=Confiq):

    app = Flask(__name__)
    app.config.from_object(Confiq)

    db.init_app(app)
    login_manager.init_app(app)

    from main.users.routes import users
    from main.posts.routes import posts
    from main.others.routes import others
    from main.errors.handlers import errors

    app.register_blueprint(users)
    app.register_blueprint(posts)
    app.register_blueprint(others)
    app.register_blueprint(errors)

    return app
