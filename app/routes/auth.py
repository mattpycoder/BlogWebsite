import logging

from flask import Blueprint, redirect, render_template, request, url_for
from flask_login import current_user, login_required, login_user, logout_user
from werkzeug.wrappers import Response

from app.database.models import User
from app.forms.auth import UserLoginForm, UserRegistrationForm
from app.utils import hash_password

logger = logging.getLogger(__name__)

auth = Blueprint("auth", __name__)


@auth.route("/login", methods=["GET", "POST"])
def login() -> str | Response:
    if current_user.is_authenticated:
        logger.info(
            f"Auth Route: Authenticated user '{current_user.username}' attempted to access /login, redirecting to profile"
        )
        return redirect(url_for("profile.profile", username=current_user.username))

    login_form = UserLoginForm()
    if request.method == "POST":
        logger.info(f"Auth Route: Processing login submission for '{login_form.email.data}'")
        if login_form.validate_on_submit():
            user = User.get_user_from_db_by_email(
                email=login_form.email.data
            ) or User.get_user_from_db_by_username(username=login_form.email.data)
            if user and user.username:
                login_user(
                    user,
                    remember=login_form.remember.data if hasattr(login_form, "remember") else False,
                )
                logger.info(
                    f"Auth Route: User '{user.username}' (ID={user.id}) successfully logged in"
                )
                return redirect(url_for("profile.profile", username=user.username))
        else:
            logger.warning(
                f"Auth Route: Login validation failed for '{login_form.email.data}'. Errors: {login_form.errors}"
            )

    return render_template("login.html", form=login_form)


@auth.route("/logout", methods=["POST"])
@login_required
def logout() -> Response:
    username = current_user.username
    logger.info(f"Auth Route: Logging out user '{username}' (ID={current_user.id})")
    logout_user()
    logger.info(f"Auth Route: User '{username}' logged out successfully")
    return redirect(url_for("auth.login"))


@auth.route("/register", methods=["GET", "POST"])
def register() -> str | Response:
    if current_user.is_authenticated:
        logger.info(
            f"Auth Route: Authenticated user '{current_user.username}' attempted to access /register, redirecting to profile"
        )
        return redirect(url_for("profile.profile", username=current_user.username))

    registration_form = UserRegistrationForm()
    if request.method == "POST":
        logger.info(
            f"Auth Route: Processing registration submission for username='{registration_form.username.data}', email='{registration_form.email.data}'"
        )
        if registration_form.validate_on_submit():
            password_hashed = hash_password(registration_form.password.data)
            user = User(
                first_name=registration_form.first_name.data,
                last_name=registration_form.last_name.data,
                username=registration_form.username.data,
                email=registration_form.email.data,
                password=password_hashed,
            )
            User.push_user_into_db(user=user)
            logger.info(
                f"Auth Route: User '{user.username}' successfully registered and saved to database"
            )
            return redirect(url_for("auth.login"))
        else:
            logger.warning(
                f"Auth Route: Registration validation failed for username='{registration_form.username.data}'. Errors: {registration_form.errors}"
            )

    return render_template("register.html", form=registration_form)
