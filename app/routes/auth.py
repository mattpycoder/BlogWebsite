from flask import Blueprint, redirect, render_template, request, url_for
from flask_login import current_user, login_required, login_user, logout_user
from werkzeug.wrappers import Response

from app.database.models import User
from app.forms.auth import UserLoginForm, UserRegistrationForm
from app.utils import hash_password

auth = Blueprint("auth", __name__)


@auth.route("/login", methods=["GET", "POST"])
def login() -> str | Response:
    if current_user.is_authenticated:
        return redirect(url_for("profile.profile"))

    login_form = UserLoginForm()
    if login_form.validate_on_submit():
        user = User.get_user_from_db_by_email(
            email=login_form.email.data
        ) or User.get_user_from_db_by_username(username=login_form.email.data)
        if user and user.username:
            login_user(user)
            return redirect(url_for("profile.profile", username=user.username))
    return render_template("login.html", form=login_form)


@auth.route("/logout", methods=["GET"])
@login_required
def logout() -> Response:
    logout_user()
    return redirect(url_for("auth.login"))


@auth.route("/register", methods=["GET", "POST"])
def register() -> str | Response:
    if current_user.is_authenticated:
        return redirect(url_for("profile.profile"))

    registration_form = UserRegistrationForm()
    if request.method == "POST" and registration_form.validate_on_submit():
        password_hashed = hash_password(registration_form.password.data)
        user = User(
            first_name=registration_form.first_name.data,
            last_name=registration_form.last_name.data,
            username=registration_form.username.data,
            email=registration_form.email.data,
            password=password_hashed,
        )
        User.push_user_into_db(user=user)
        return redirect(url_for("auth.login"))
    return render_template("register.html", form=registration_form)
