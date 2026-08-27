from flask import Blueprint, make_response, render_template
from flask_login import login_required
from werkzeug import Response

profile_bp = Blueprint("profile", __name__)


@profile_bp.route("/profile", methods=["GET", "POST"])
@login_required
def profile() -> Response:
    response = make_response(render_template("profile.html"))
    response.cache_control.no_store = True
    return response
