from __future__ import annotations

from datetime import UTC, datetime
from typing import Any

from flask_login import UserMixin
from sqlalchemy.orm import Mapped
from sqlalchemy.testing.schema import mapped_column

from app.extensions import db


class User(db.Model, UserMixin):  # ty: ignore[unsupported-base]
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True)
    username: Mapped[str] = mapped_column(unique=True, nullable=False)
    first_name: Mapped[str] = mapped_column(nullable=True)
    last_name: Mapped[str] = mapped_column(nullable=True)
    email: Mapped[str] = mapped_column(unique=True, nullable=False)
    password: Mapped[str] = mapped_column(nullable=False)
    created_at: Mapped[datetime] = mapped_column(
        nullable=False,
        default=lambda: datetime.now(UTC),
    )

    @staticmethod
    def push_user_into_db(user: User) -> None:
        db.session.add(user)
        db.session.commit()

    @staticmethod
    def is_field_in_db(**kwargs: Any) -> bool:
        return db.session.scalar(db.select(User).filter_by(**kwargs)) is not None

    @staticmethod
    def get_user_from_db_by_email(email: str) -> User | None:
        return db.session.scalar(db.select(User).filter_by(email=email))

    @staticmethod
    def get_user_from_db_by_username(username: str) -> User | None:
        return db.session.scalar(db.select(User).filter_by(username=username))
