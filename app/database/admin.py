from flask import redirect, url_for
from flask_admin import AdminIndexView
from flask_login import current_user
from werkzeug.exceptions import abort


class MyAdminIndexView(AdminIndexView):
    def is_accessible(self):
        return current_user.is_authenticated and current_user.is_admin

    def inaccessible_callback(self, name, **kwargs):
        if not current_user.is_authenticated:
            return redirect(url_for("login"))

        abort(403)
