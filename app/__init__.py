from flask import Flask
from flask_login import LoginManager

from app.config import Config
from app.database.models import User
from app.extensions import bcrypt, csrf, db, migrate
from app.routes.auth import auth
from app.routes.general import general_bp
from app.routes.profile import profile_bp


def create_app() -> Flask:
    app = Flask(__name__)
    app.config.from_object(Config)

    login_manager = LoginManager()
    login_manager.init_app(app)
    login_manager.login_view = "auth.login"

    @login_manager.user_loader
    def load_user(user_id) -> User | None:
        return db.session.get(User, int(user_id))

    db.init_app(app)
    migrate.init_app(app, db)
    bcrypt.init_app(app)
    csrf.init_app(app)

    app.register_blueprint(auth)
    app.register_blueprint(general_bp)
    app.register_blueprint(profile_bp)
    return app
