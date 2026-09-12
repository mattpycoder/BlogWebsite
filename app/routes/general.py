import logging

from flask import Blueprint, render_template

logger = logging.getLogger(__name__)

general_bp = Blueprint("general", __name__, template_folder="templates")


@general_bp.route("/")
def index() -> str:
    logger.info("General Route: Serving homepage '/'")
    return render_template("index.html")


@general_bp.errorhandler(404)
def page_not_found(e) -> tuple[str, int]:
    return render_template("404.html"), 404
