from flask import Blueprint, redirect, url_for
from flask_login import login_required, logout_user
from werkzeug.wrappers import Response

logout_bp = Blueprint("logout", __name__)


@logout_bp.route("/logout", methods=["GET"])
@login_required
def logout() -> Response:
    logout_user()
    return redirect(url_for("login.login"))
