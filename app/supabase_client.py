import logging

from flask_login import current_user
from storage3.exceptions import StorageException
from storage3.types import FileOptions
from supabase import create_client
from supabase.client import ClientOptions
from werkzeug.datastructures import FileStorage

from app import Config

logger = logging.getLogger(__name__)


class SupabaseClient:
    def __init__(self, bucket_name: str = Config.SUPABASE_BUCKET_NAME):
        self.client = create_client(
            supabase_url=f"https://{Config.SUPABASE_PROJECT_ID}.supabase.co",
            supabase_key=Config.SUPABASE_API_KEY,
            options=ClientOptions(
                storage_client_timeout=10,
                schema="public",
            ),
        )
        self.bucket_name = bucket_name

    def upload_profile_picture(self, path: str, profile_picture: FileStorage) -> None:
        logger.info(f"Supabase: Uploading profile_picture: {path}")
        content_type = profile_picture.content_type
        if content_type is None:
            raise ValueError("Profile picture content type is missing")
        file_options: FileOptions = {
            "content-type": content_type,
            "upsert": "true",
        }
        self.client.storage.from_(self.bucket_name).upload(
            path=path, file=profile_picture.read(), file_options=file_options
        )
        logger.info(f"Supabase: Uploaded profile_picture: {path}")

    @staticmethod
    def get_profile_picture_url() -> str:
        logger.info("Constructing Profile Picture URL")
        profile_picture_url = (
            f"https://{Config.SUPABASE_PROJECT_ID}.supabase.co/storage/v1/object/public/"
            f"{Config.SUPABASE_BUCKET_NAME}/avatars/{current_user.id}/profile.jpg"
        )
        return profile_picture_url

    def delete_profile_picture(self, path: str) -> None:
        logger.info("Supabase: Deleting Profile Picture...")
        try:
            self.client.storage.from_(self.bucket_name).remove([path])
        except StorageException as e:
            logger.error(f"Supabase: Failed to delete profile picture at {path}: {e}")
        logger.info("Supabase: Profile Picture is successfully deleted")
