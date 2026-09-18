import logging

from app.extensions import bcrypt

logger = logging.getLogger(__name__)


def hash_password(password: str) -> str:
    logger.debug("Bcrypt: Generating password hash")
    return bcrypt.generate_password_hash(password).decode("utf-8")


def check_password(password_hash: str, password: str) -> bool:
    is_valid = bcrypt.check_password_hash(pw_hash=password_hash, password=password)
    logger.debug(f"Bcrypt: Password verification result={is_valid}")
    return is_valid
