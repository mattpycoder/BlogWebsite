from flask import Flask
from flask_login import LoginManager

from app.database.config import Config
from app.database.extensions import bcrypt, db
from app.database.models import User
from app.routes.general import general_bp
from app.routes.login import login_bp
from app.routes.logout import logout_bp
from app.routes.profile import profile_bp
from app.routes.register import register_bp


def create_app() -> Flask:
    app = Flask(__name__)
    app.config.from_object(Config)
    app.config["SECRET_KEY"] = "LongAndRandomSecretKey"

    login_manager = LoginManager()
    login_manager.init_app(app)
    login_manager.login_view = "login.login"

    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))

    db.init_app(app)
    bcrypt.init_app(app)

    app.register_blueprint(login_bp)

    app.register_blueprint(register_bp)
    app.register_blueprint(general_bp)
    app.register_blueprint(profile_bp)
    app.register_blueprint(logout_bp)
    return app
