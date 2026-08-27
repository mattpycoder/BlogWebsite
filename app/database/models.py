from __future__ import annotations

from typing import Any

from flask_login import UserMixin

from app.database.extensions import db


class User(db.Model, UserMixin):  # ty: ignore[unsupported-base]
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), unique=True, nullable=False)
    first_name = db.Column(db.String(100), nullable=True)
    last_name = db.Column(db.String(100), nullable=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)

    @staticmethod
    def push_user_into_db(user: User) -> None:
        db.session.add(user)
        db.session.commit()

    @staticmethod
    def is_field_exists_in_db(**kwargs: dict[str, Any]) -> bool:
        return User.query.filter_by(**kwargs).first()

    @staticmethod
    def get_user_by_email_from_db(email: str) -> User | None:
        user = User.query.filter_by(email=email).first()
        return user
