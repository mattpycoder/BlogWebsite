import logging

from flask import Blueprint, render_template

logger = logging.getLogger(__name__)

general_bp = Blueprint("general", __name__, template_folder="templates")


@general_bp.route("/")
def index() -> str:
    logger.info("General Route: Serving homepage '/'")
    return render_template("index.html")


@general_bp.errorhandler(403)
def forbidden(e) -> tuple[str, int]:
    logger.warning(f"Error Handler: 403 Forbidden encountered: {e}")
    return render_template("403.html"), 403


@general_bp.errorhandler(404)
def page_not_found(e) -> tuple[str, int]:
    logger.warning(f"Error Handler: 404 Not Found encountered: {e}")
    return render_template("404.html"), 404


@general_bp.errorhandler(500)
def internal_server_error(e) -> tuple[str, int]:
    logger.error(f"Error Handler: 500 Internal Server Error encountered: {e}")
    return render_template("500.html"), 500
