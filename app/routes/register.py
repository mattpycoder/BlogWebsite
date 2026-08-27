from typing import cast

from flask import Blueprint, redirect, render_template, url_for
from flask_login import current_user
from werkzeug.wrappers import Response

from app.database.models import User
from app.forms.register import UserRegistrationForm
from app.utils import hash_password

register_bp = Blueprint("register", __name__)


@register_bp.route("/register", methods=["GET", "POST"])
def register() -> str | Response:
    if current_user.is_authenticated:
        return redirect(url_for("profile.profile"))
    registration_form = UserRegistrationForm()
    if registration_form.validate_on_submit():
        if User.is_field_exists_in_db(username=registration_form.username.data):
            cast(list[str], registration_form.username.errors).append(
                "Username is already registered."
            )
        elif User.is_field_exists_in_db(email=registration_form.email.data):
            cast(list[str], registration_form.email.errors).append("Email is already registered.")
        else:
            password_hashed = hash_password(registration_form.password.data)
            user = User(
                first_name=registration_form.first_name.data,
                last_name=registration_form.last_name.data,
                username=registration_form.username.data,
                email=registration_form.email.data,
                password=password_hashed,
            )
            User.push_user_into_db(user=user)
            return redirect(url_for("login.login"))
    return render_template("register.html", form=registration_form)
