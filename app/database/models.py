from __future__ import annotations

import logging
from datetime import UTC, datetime
from typing import Any

from flask_login import UserMixin
from sqlalchemy.orm import Mapped
from sqlalchemy.testing.schema import mapped_column

from app.extensions import db
from app.utils import hash_password

logger = logging.getLogger(__name__)


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
        logger.info(
            f"Database: Saving new user to DB with username='{user.username}', email='{user.email}'"
        )
        try:
            db.session.add(user)
            db.session.commit()
            logger.info(f"Database: User '{user.username}' successfully created with ID={user.id}")
        except Exception:
            db.session.rollback()
            logger.exception(f"Database Error: Failed to add user '{user.username}'")
            raise

    @staticmethod
    def is_field_in_db(**kwargs: Any) -> bool:
        exists = db.session.scalar(db.select(User).filter_by(**kwargs)) is not None
        logger.debug(f"Database: Querying existence for filter={kwargs} -> Result: {exists}")
        return exists

    @staticmethod
    def get_user_from_db_by_email(email: str) -> User | None:
        user = db.session.scalar(db.select(User).filter_by(email=email))
        if user:
            logger.debug(
                f"Database: Found user by email='{email}' -> User(id={user.id}, username='{user.username}')"
            )
        else:
            logger.debug(f"Database: No user found for email='{email}'")
        return user

    @staticmethod
    def get_user_from_db_by_username(username: str) -> User | None:
        user = db.session.scalar(db.select(User).filter_by(username=username))
        if user:
            logger.debug(f"Database: Found user by username='{username}' -> User(id={user.id})")
        else:
            logger.debug(f"Database: No user found for username='{username}'")
        return user

    def change_user_password(self, new_password: str) -> None:
        logger.info(f"Database: Updating password for user '{self.username}' (ID={self.id})")
        try:
            self.password = hash_password(new_password)
            db.session.commit()
            logger.info(
                f"Database: Password update committed successfully for user '{self.username}'"
            )
        except Exception:
            db.session.rollback()
            logger.exception(
                f"Database Error: Failed to update password for user '{self.username}'",
            )
            raise
