from flask_admin import Admin
from flask_bcrypt import Bcrypt
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import CSRFProtect
from sqlalchemy.orm import DeclarativeBase

from app.database.admin import MyAdminIndexView
from app.supabase_client import SupabaseClient


class Base(DeclarativeBase):
    pass


db = SQLAlchemy(model_class=Base)
migrate = Migrate()
bcrypt = Bcrypt()
csrf = CSRFProtect()
supabase_client = SupabaseClient()
admin = Admin(name="Blog Website Admin", index_view=MyAdminIndexView())
