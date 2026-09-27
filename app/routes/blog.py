import logging

from flask import Blueprint, flash, redirect, render_template, url_for
from flask_login import current_user, login_required
from werkzeug.wrappers import Response

from app.database.models import Blog
from app.forms.blog import CreateBlogForm

logger = logging.getLogger(__name__)

blog_bp = Blueprint("blogs", __name__, template_folder="templates")


@blog_bp.route("/<username>/profile/blog/create", methods=["POST"])
@login_required
def create_blog(username: str) -> str | tuple[str, int] | Response:
    if current_user.username != username:
        return render_template("403.html"), 403

    create_blog_form = CreateBlogForm()
    if create_blog_form.validate_on_submit():
        blog = Blog(
            user_id=current_user.id,
            title=create_blog_form.title.data,
            category=create_blog_form.category.data,
            description=create_blog_form.description.data,
        )
        blog.add_blog_to_db()
        flash(f"Blog '{blog.title}' created successfully!", "success")
        return redirect(url_for("profile.profile", username=current_user.username))

    return render_template(
        "profile.html",
        profile_user=username,
        is_owner=True,
        profile_picture_url=current_user.profile_picture_url,
        create_blog_form=create_blog_form,
        blogs=current_user.blogs,
        posts=current_user.posts,
        active_tab="blogs-tab",
    )
