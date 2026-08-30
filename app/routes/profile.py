from flask import Blueprint, make_response, render_template
from flask_login import current_user, login_required
from werkzeug import Response

from app.database.models import User

profile_bp = Blueprint("profile", __name__)


@profile_bp.route("/profile/<username>", methods=["GET"])
@login_required
def profile(username: str) -> Response | str:
    if User.is_field_in_db(username=username):
        is_owner = current_user.username == username
        response = make_response(
            render_template(
                "profile.html",
                profile_user=username,
                is_owner=is_owner,
            )
        )
        response.cache_control.no_store = True
        return response
    return render_template("404.html")
