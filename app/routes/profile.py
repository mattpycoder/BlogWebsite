import logging

from flask import Blueprint, flash, make_response, redirect, render_template, url_for
from flask_login import current_user, login_required, logout_user
from werkzeug import Response

from app.database.models import User
from app.extensions import supabase_client
from app.forms.auth import UserChangePasswordForm, UserProfileInfoForm, UserUpdateProfilePictureForm

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
        profile_picture_url = current_user.profile_picture
        if profile_picture_url:
            profile_picture_url = supabase_client.get_profile_picture_url()
            logger.info(f"Profile Picture URL: {profile_picture_url}")
        response = make_response(
            render_template(
                "profile.html",
                profile_user=username,
                is_owner=is_owner,
                profile_picture_url=profile_picture_url,
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


@profile_bp.route("/delete_account", methods=["POST"])
@login_required
def delete_account() -> str:
    current_user.delete_user()
    flash("Your account has been deleted successfully.", "success")
    logout_user()
    return render_template("login.html")


@profile_bp.route("/update_profile_picture", methods=["POST"])
@login_required
def update_profile_picture() -> Response:
    update_profile_form = UserUpdateProfilePictureForm()
    profile_picture_path = f"avatars/{current_user.id}/profile.jpg"
    profile_picture_url = supabase_client.get_profile_picture_url()
    if update_profile_form.validate_on_submit():
        supabase_client.upload_profile_picture(
            path=profile_picture_path, profile_picture=update_profile_form.profile_picture.data
        )
        current_user.update_profile_picture(profile_picture_path=profile_picture_path)
        flash("Profile picture updated successfully.", "success")
    return redirect(
        url_for(
            "profile.profile",
            username=current_user.username,
            is_owner=True,
            profile_picture_url=profile_picture_url,
        )
    )


@profile_bp.route("/delete_profile_picture", methods=["POST"])
@login_required
def delete_profile_picture() -> Response:
    path = current_user.profile_picture
    if path:
        supabase_client.delete_profile_picture(path=current_user.profile_picture)
        current_user.delete_profile_picture()
    flash("Profile picture removed successfully.", "success")
    return redirect(url_for("profile.profile", username=current_user.username, is_owner=True))


@profile_bp.route("/update_profile_info", methods=["POST"])
@login_required
def update_profile_info() -> Response:
    update_profile_info_form = UserProfileInfoForm()
    if update_profile_info_form.validate_on_submit():
        if update_profile_info_form.first_name.data != current_user.first_name:
            current_user.update_first_name(first_name=update_profile_info_form.first_name.data)
            flash("Profile first name updated successfully.", "success")
        if update_profile_info_form.last_name.data != current_user.last_name:
            current_user.update_last_name(last_name=update_profile_info_form.last_name.data)
            flash("Profile last name updated successfully.", "success")
        if update_profile_info_form.bio.data != current_user.bio:
            current_user.update_bio(bio=update_profile_info_form.bio.data)
            flash("Profile bio updated successfully.", "success")
    return redirect(url_for("profile.profile", username=current_user.username, is_owner=True))
