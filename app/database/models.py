from __future__ import annotations

import logging
from datetime import UTC, datetime
from typing import Any

from flask_login import UserMixin
from sqlalchemy.orm import Mapped, relationship
from sqlalchemy.testing.schema import mapped_column

from app.extensions import db, supabase_client
from app.utils import hash_password

logger = logging.getLogger(__name__)


class User(db.Model, UserMixin):  # ty: ignore[unsupported-base]
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True)
    username: Mapped[str] = mapped_column(unique=True, nullable=False)
    first_name: Mapped[str] = mapped_column(nullable=False)
    last_name: Mapped[str] = mapped_column(nullable=False)
    email: Mapped[str] = mapped_column(unique=True, nullable=False)
    password: Mapped[str] = mapped_column(nullable=False)
    created_at: Mapped[datetime] = mapped_column(
        nullable=False,
        default=lambda: datetime.now(UTC),
    )
    is_admin: Mapped[bool] = mapped_column(default=False)
    bio: Mapped[str] = mapped_column(nullable=True)
    profile_picture: Mapped[str] = mapped_column(nullable=True)
    blogs: Mapped[list[Blog]] = relationship(back_populates="user", cascade="all, delete-orphan")
    posts: Mapped[list[Post]] = relationship(back_populates="user", cascade="all, delete-orphan")

    @property
    def profile_picture_url(self) -> str:
        return supabase_client.get_profile_picture_url(user_id=self.id)

    @staticmethod
    def add_user_to_db(user: User) -> None:
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

    def delete_user(self) -> None:
        logger.info(f"Database: Deleting operation for user '{self.username}' (ID={self.id})")
        try:
            db.session.delete(self)
            db.session.commit()
            logger.info("Database: The user is successfully deleted")
        except Exception:
            db.session.rollback()
            logger.exception(
                f"Database Error: Failed to delete the user '{self.username}'",
            )
            raise

    def update_profile_picture(self, profile_picture_path: str) -> None:
        logger.info(f"Database: Updating profile picture for user '{self.username}'")
        try:
            self.profile_picture = profile_picture_path
            db.session.commit()
            logger.info(
                f"Database: Profile picture path update committed successfully for user '{self.username}'"
            )
        except Exception:
            db.session.rollback()
            logger.exception(
                f"Database Error: Failed to update profile picture path for user '{self.username}'",
            )
            raise

    def delete_profile_picture(self) -> None:
        logger.info(f"Database: Deleting profile picture for user '{self.username}'")
        try:
            self.profile_picture = ""
            db.session.commit()
            logger.info(
                f"Database: Profile picture path deletion committed successfully for user '{self.username}'"
            )
        except Exception:
            db.session.rollback()
            logger.exception(
                f"Database Error: Failed to delete profile picture path for user '{self.username}'",
            )
            raise

    def update_profile_info(self) -> None:
        logger.info(f"Database: Updating profile info for user '{self.username}'")

        if not db.session.is_modified(self):
            return

        try:
            db.session.commit()
            logger.info("Profile info updated successfully!")
        except Exception:
            db.session.rollback()
            logger.exception(
                f"Database Error: Failed to update profile info for user '{self.username}'"
            )
            raise


class Blog(db.Model):  # ty: ignore[unsupported-base]
    __tablename__ = "blogs"

    id: Mapped[int] = mapped_column(primary_key=True)

    user_id: Mapped[int] = mapped_column(
        db.ForeignKey("users.id"),
        nullable=False,
    )

    title: Mapped[str] = mapped_column(
        nullable=False,
    )

    category: Mapped[str] = mapped_column(
        nullable=False,
    )

    description: Mapped[str] = mapped_column(
        nullable=False,
    )

    created_at: Mapped[datetime] = mapped_column(
        nullable=False,
        default=lambda: datetime.now(UTC),
    )

    updated_at: Mapped[datetime] = mapped_column(
        nullable=False,
        default=lambda: datetime.now(UTC),
        onupdate=lambda: datetime.now(UTC),
    )

    user: Mapped[User] = relationship(
        back_populates="blogs",
    )

    posts: Mapped[list[Post]] = relationship(
        back_populates="blog",
        cascade="all, delete-orphan",
    )

    def add_blog_to_db(self) -> None:
        logger.info("Database: Adding blog to database")
        try:
            db.session.add(self)
            db.session.commit()
            logger.info("Database: The blog is successfully added to database")
        except Exception:
            db.session.rollback()
            logger.exception(
                "Database Error: Failed to add the blog to database",
            )
            raise


class Post(db.Model):  # ty: ignore[unsupported-base]
    __tablename__ = "posts"

    id: Mapped[int] = mapped_column(primary_key=True)

    blog_id: Mapped[int] = mapped_column(
        db.ForeignKey("blogs.id"),
        nullable=False,
    )

    user_id: Mapped[int] = mapped_column(
        db.ForeignKey("users.id"),
        nullable=False,
    )

    title: Mapped[str] = mapped_column(
        nullable=False,
    )

    content: Mapped[str] = mapped_column(
        db.Text,
        nullable=False,
    )

    created_at: Mapped[datetime] = mapped_column(
        nullable=False,
        default=lambda: datetime.now(UTC),
    )

    updated_at: Mapped[datetime] = mapped_column(
        nullable=False,
        default=lambda: datetime.now(UTC),
        onupdate=lambda: datetime.now(UTC),
    )

    blog: Mapped[Blog] = relationship(
        back_populates="posts",
    )

    user: Mapped[User] = relationship(
        back_populates="posts",
    )

    def add_post_to_db(self) -> None:
        logger.info(f"Database: Adding post '{self.title}' to database")
        try:
            db.session.add(self)
            db.session.commit()
            logger.info(f"Database: Post '{self.title}' successfully added with ID={self.id}")
        except Exception:
            db.session.rollback()
            logger.exception(f"Database Error: Failed to add post '{self.title}' to database")
            raise

    @staticmethod
    def get_post_by_id(post_id: int) -> Post | None:
        return db.session.scalar(db.select(Post).filter_by(id=post_id))

    def delete_post_from_db(self) -> None:
        logger.info(f"Database: Deleting post '{self.title}' (ID={self.id})")
        try:
            db.session.delete(self)
            db.session.commit()
            logger.info(f"Database: Post '{self.title}' successfully deleted")
        except Exception:
            db.session.rollback()
            logger.exception(f"Database Error: Failed to delete post '{self.title}'")
            raise
