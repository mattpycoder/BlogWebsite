import logging

from flask import Blueprint, flash, make_response, redirect, render_template, url_for
from flask_login import current_user, login_required
from werkzeug import Response

from app.database.models import User
from app.forms.auth import UserChangePasswordForm

logger = logging.getLogger(__name__)

profile_bp = Blueprint("profile", __name__)


@profile_bp.route("/<username>/profile", methods=["GET"])
@login_required
def profile(username: str) -> Response | tuple[str, int]:
    logger.info(
        f"Profile Route: User '{current_user.username}' requested profile view for username='{username}'"
    )
    if User.is_field_in_db(username=username):
        is_owner = current_user.username == username
        logger.debug(f"Profile Route: Profile found for '{username}', is_owner={is_owner}")
        response = make_response(
            render_template(
                "profile.html",
                profile_user=username,
                is_owner=is_owner,
            )
        )
        response.cache_control.no_store = True
        return response

    logger.warning(f"Profile Route: Profile not found for username='{username}', rendering 404")
    return render_template("404.html"), 404


@profile_bp.route("/change_password", methods=["POST"])
@login_required
def change_password() -> Response | str:
    logger.info(
        f"Password Change Route: Processing password change request for user '{current_user.username}'"
    )
    change_password_form = UserChangePasswordForm()

    if change_password_form.validate_on_submit():
        user = User.get_user_from_db_by_username(username=current_user.username)
        if user:
            user.change_user_password(new_password=change_password_form.new_password.data)
            logger.info(
                f"Password Change Route: Password changed successfully for user '{current_user.username}'"
            )
            flash("Your password has been updated successfully.", "success")
            return redirect(url_for("profile.profile", username=current_user.username))
        else:
            logger.error(
                f"Password Change Route: User '{current_user.username}' not found in database during password update"
            )
            flash("An error occurred while updating your password. Please try again.", "danger")
            return redirect(url_for("profile.profile", username=current_user.username))

    logger.warning(
        f"Password Change Route: Validation failed for user '{current_user.username}'. Errors: {change_password_form.errors}"
    )
    return render_template(
        "profile.html",
        username=current_user.username,
        change_password_form=change_password_form,
        is_owner=True,
        active_tab="settings-tab",
    )
