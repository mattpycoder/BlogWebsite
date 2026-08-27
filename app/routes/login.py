from typing import cast

from flask import Blueprint, redirect, render_template, url_for
from flask_login import current_user, login_user
from werkzeug.wrappers import Response

from app.database.models import User
from app.forms.login import UserLoginForm
from app.utils import check_password

login_bp = Blueprint("login", __name__)


@login_bp.route("/login", methods=["GET", "POST"])
def login() -> str | Response:
    if current_user.is_authenticated:
        return redirect(url_for("profile.profile"))
    login_form = UserLoginForm()
    if login_form.validate_on_submit():
        user = User.get_user_by_email_from_db(email=login_form.email.data)
        if user and check_password(user.password, login_form.password.data):
            login_user(user)
            return redirect(url_for("profile.profile"))
        cast(list[str], login_form.password.errors).append("Invalid username or password")
    return render_template("login.html", form=login_form)
