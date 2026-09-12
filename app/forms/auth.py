import logging

from flask_login import current_user
from flask_wtf import FlaskForm
from wtforms.fields.simple import BooleanField, PasswordField, StringField, SubmitField
from wtforms.validators import DataRequired, Email, EqualTo, Length, Regexp, ValidationError

from app.database.models import User
from app.utils import check_password

logger = logging.getLogger(__name__)

RESERVED_USERNAMES = {
    "admin",
    "administrator",
    "root",
    "system",
    "support",
    "api",
    "register",
    "logout",
    "profile",
    "static",
}


class UserLoginForm(FlaskForm):
    email = StringField("Email", validators=[DataRequired(), Length(max=64)])
    password = PasswordField("Password", validators=[DataRequired(), Length(min=8)])
    remember = BooleanField("Remember me")
    submit = SubmitField(label=("Sign In"))

    def validate_email(self, username: StringField) -> None:
        logger.debug(f"Form Validation: Checking user identifier '{username.data}' for login")
        user = User.get_user_from_db_by_email(
            email=username.data
        ) or User.get_user_from_db_by_username(username=username.data)
        if not user:
            logger.warning(
                f"Form Validation Failed: User with identifier '{username.data}' not found in database"
            )
            raise ValidationError("Invalid username or email.")

    def validate_password(self, password: PasswordField) -> None:
        login = self.email.data
        logger.debug(f"Form Validation: Verifying password for '{login}'")
        user = User.get_user_from_db_by_email(email=login) or User.get_user_from_db_by_username(
            username=login
        )
        if not user or not check_password(user.password, password.data):
            logger.warning(f"Form Validation Failed: Incorrect password attempt for '{login}'")
            raise ValidationError("Invalid password.")


class UserRegistrationForm(FlaskForm):
    first_name = StringField("First Name", validators=[Length(max=100)])
    last_name = StringField("Last Name", validators=[Length(max=100)])
    username = StringField(
        "Username",
        validators=[
            DataRequired(),
            Length(min=8, max=64),
            Regexp(
                r"^[A-Za-z0-9](?:[A-Za-z0-9_]*[A-Za-z0-9])?$",
                message=(
                    "Username must contain only letters, numbers, "
                    "and underscores, and cannot start or end with an underscore."
                ),
            ),
        ],
    )
    email = StringField("Email", validators=[DataRequired(), Email()])
    password = PasswordField("Password", validators=[DataRequired(), Length(min=8, max=80)])
    confirm_password = PasswordField(
        "Confirm Password", validators=[DataRequired(), EqualTo("password")]
    )
    submit = SubmitField(label=("Submit"))

    def validate_username(self, username: StringField) -> None:
        if username.data.lower() in RESERVED_USERNAMES:
            logger.warning(f"Form Validation Failed: Reserved username requested '{username.data}'")
            raise ValidationError("This username is not available.")
        if username.data and User.is_field_in_db(username=username.data):
            logger.warning(
                f"Form Validation Failed: Duplicate username registration attempt '{username.data}'"
            )
            raise ValidationError("Username is already registered.")

    def validate_email(self, email: StringField) -> None:
        if email.data and User.is_field_in_db(email=email.data):
            logger.warning(
                f"Form Validation Failed: Duplicate email registration attempt '{email.data}'"
            )
            raise ValidationError("Email is already registered.")


class UserChangePasswordForm(FlaskForm):
    current_password = PasswordField(
        "Current Password", validators=[DataRequired(), Length(min=8, max=80)]
    )
    new_password = PasswordField("New Password", validators=[DataRequired(), Length(min=8, max=80)])
    confirm_password = PasswordField(
        "Confirm Password", validators=[DataRequired(), EqualTo("new_password")]
    )
    submit = SubmitField(label=("Submit"))

    def validate_current_password(self, current_password: PasswordField) -> None:
        logger.debug(
            f"Form Validation: Verifying current password for user '{current_user.username}'"
        )
        user = User.get_user_from_db_by_username(username=current_user.username)
        if not user or not check_password(user.password, current_password.data):
            logger.warning(
                f"Form Validation Failed: Incorrect current password entered for user '{current_user.username}'"
            )
            raise ValidationError("Current password is incorrect.")

    def validate_new_password(self, new_password: PasswordField) -> None:
        user = User.get_user_from_db_by_username(username=current_user.username)
        if user and check_password(user.password, new_password.data):
            logger.warning(
                f"Form Validation Failed: User '{current_user.username}' entered existing password as new password"
            )
            raise ValidationError("New password must be different from your current password.")
