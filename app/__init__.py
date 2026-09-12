import logging

from flask import Flask, flash, redirect, request, url_for
from flask_login import LoginManager

from app.config import Config
from app.database.models import User
from app.extensions import bcrypt, csrf, db, migrate
from app.routes.auth import auth
from app.routes.general import general_bp, page_not_found
from app.routes.profile import profile_bp

logger = logging.getLogger(__name__)


def create_app() -> Flask:
    # Configure root logger with a clear, timestamped format
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s [%(levelname)s] (%(name)s): %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )

    app = Flask(__name__)
    app.config.from_object(Config)
    logger.info("Application: Initializing Flask application factory")

    login_manager = LoginManager()
    login_manager.init_app(app)
    login_manager.login_view = "auth.login"

    @login_manager.user_loader
    def load_user(user_id) -> User | None:
        logger.debug(f"LoginManager: Loading user from session with ID={user_id}")
        return db.session.get(User, int(user_id))

    @login_manager.unauthorized_handler
    def unauthorized():
        logger.warning(
            f"LoginManager: Unauthorized access attempt to '{request.path}' from IP '{request.remote_addr}'"
        )
        flash("Please log in to access this page.", "info")
        return redirect(url_for("auth.login"))

    db.init_app(app)
    migrate.init_app(app, db)
    bcrypt.init_app(app)
    csrf.init_app(app)
    logger.info("Application: Database, Migrate, Bcrypt, and CSRF extensions initialized")

    app.register_blueprint(auth)
    app.register_blueprint(general_bp)
    app.register_blueprint(profile_bp)
    app.register_error_handler(404, page_not_found)
    logger.info("Application: Registered Blueprints (auth, general, profile)")

    return app
