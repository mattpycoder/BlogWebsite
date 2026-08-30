from flask import Flask
from flask_login import LoginManager

from app.database.config import Config
from app.database.extensions import bcrypt, db, migrate
from app.database.models import User
from app.routes.auth import auth
from app.routes.general import general_bp
from app.routes.profile import profile_bp


def create_app() -> Flask:
    app = Flask(__name__)
    app.config.from_object(Config)
    app.config["SECRET_KEY"] = "LongAndRandomSecretKey"

    login_manager = LoginManager()
    login_manager.init_app(app)
    login_manager.login_view = "auth.login"

    @login_manager.user_loader
    def load_user(user_id) -> User | None:
        return db.session.get(User, int(user_id))

    db.init_app(app)
    migrate.init_app(app, db)
    bcrypt.init_app(app)

    app.register_blueprint(auth)
    app.register_blueprint(general_bp)
    app.register_blueprint(profile_bp)
    return app
