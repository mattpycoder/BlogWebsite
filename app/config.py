import os

from dotenv import load_dotenv

load_dotenv()


class Config:
    SQLALCHEMY_DATABASE_URI = os.environ["SQLALCHEMY_DATABASE_URI"]
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = os.environ["SECRET_KEY"]
    SUPABASE_BUCKET_NAME = os.environ["SUPABASE_BUCKET_NAME"]
    SUPABASE_PROJECT_ID = os.environ["SUPABASE_PROJECT_ID"]
    SUPABASE_API_KEY = os.environ["SUPABASE_API_KEY"]
