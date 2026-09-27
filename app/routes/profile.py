import logging

from flask import Blueprint, abort, flash, make_response, redirect, render_template, url_for
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
    user = User.get_user_from_db_by_username(username=username)
    if user:
        is_owner = current_user.username == username
        logger.debug(f"Profile Route: Profile found for '{username}', is_owner={is_owner}")
        does_user_have_profile_picture = user.profile_picture
        logger.info(f"user profile picture url form db: {does_user_have_profile_picture}")
        profile_picture_url = user.profile_picture_url
        logger.info(f"Profile Picture URL: {profile_picture_url}")
        response = make_response(
            render_template(
                "profile.html",
                user=user,
                is_owner=is_owner,
                profile_picture_url=profile_picture_url,
                blogs=user.blogs,
                posts=user.posts,
            )
        )
        response.cache_control.no_store = True
        return response

    logger.warning(f"Profile Route: Profile not found for username='{username}', rendering 404")
    return render_template("404.html"), 404


@profile_bp.route("/<username>/profile/change_password", methods=["POST"])
@login_required
def change_password(username: str) -> Response | str:
    if current_user.username != username:
        abort(403)

    logger.info(
        f"Password Change Route: Processing password change request for user '{current_user.username}'"
    )
    change_password_form = UserChangePasswordForm()

    if change_password_form.validate_on_submit():
        current_user.change_user_password(new_password=change_password_form.new_password.data)
        logger.info(
            f"Password Change Route: Password changed successfully for user '{current_user.username}'"
        )
        flash("Your password has been updated successfully.", "success")
        return redirect(url_for("profile.profile", username=current_user.username))

    logger.warning(
        f"Password Change Route: Validation failed for user '{current_user.username}'. Errors: {change_password_form.errors}"
    )
    return render_template(
        "profile.html",
        username=current_user.username,
        profile_user=current_user.username,
        change_password_form=change_password_form,
        is_owner=True,
        profile_picture_url=current_user.profile_picture_url,
        blogs=current_user.blogs,
        posts=current_user.posts,
        active_tab="settings-tab",
    )


@profile_bp.route("/<username>/profile/delete_account", methods=["POST"])
@login_required
def delete_account(username: str) -> Response:
    if current_user.username != username:
        abort(403)

    path = current_user.profile_picture
    current_user.delete_user()
    supabase_client.delete_profile_picture(path=path)
    flash("Your account has been deleted successfully.", "success")
    logout_user()
    return redirect(url_for("auth.login"))


@profile_bp.route("/<username>/profile/update_profile_picture", methods=["POST"])
@login_required
def update_profile_picture(username: str) -> Response:
    if current_user.username != username:
        abort(403)

    update_profile_form = UserUpdateProfilePictureForm()
    profile_picture_path = f"avatars/{current_user.id}/profile.jpg"
    profile_picture_url = supabase_client.get_profile_picture_url(user_id=current_user.id)
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


@profile_bp.route("/<username>/profile/delete_profile_picture", methods=["POST"])
@login_required
def delete_profile_picture(username: str) -> Response:
    if current_user.username != username:
        abort(403)

    path = current_user.profile_picture
    if path:
        supabase_client.delete_profile_picture(path=current_user.profile_picture)
        current_user.delete_profile_picture()
    flash("Profile picture removed successfully.", "success")
    return redirect(url_for("profile.profile", username=current_user.username, is_owner=True))


@profile_bp.route("/<username>/profile/update_profile_info", methods=["POST"])
@login_required
def update_profile_info(username: str) -> str | Response:
    if current_user.username != username:
        abort(403)

    update_profile_info_form = UserProfileInfoForm()
    if update_profile_info_form.validate_on_submit():
        update_profile_info_form.populate_obj(current_user)
        current_user.update_profile_info()
        flash("Profile updated successfully!", "success")
        return redirect(url_for("profile.profile", username=current_user.username, is_owner=True))
    return render_template(
        "profile.html", username=current_user.username, is_owner=True, active_tab="settings-tab"
    )
