import logging

from flask import Blueprint, flash, redirect, render_template, request, url_for
from flask_login import current_user, login_required
from werkzeug.wrappers import Response

from app.database.models import Post
from app.forms.blog import CreatePostForm

logger = logging.getLogger(__name__)

post_bp = Blueprint("posts", __name__, template_folder="templates")


@post_bp.route("/post/create", methods=["GET", "POST"])
@login_required
def create_post() -> str | Response:
    user_blogs = current_user.blogs
    if not user_blogs:
        flash("You need to create at least one blog before writing a post.", "info")
        return redirect(url_for("profile.profile", username=current_user.username))

    create_post_form = CreatePostForm()
    create_post_form.blog_id.choices = [(blog.id, blog.title) for blog in user_blogs]

    if request.method == "GET" and request.args.get("blog_id"):
        blog_id = request.args.get("blog_id")
        if blog_id:
            try:
                request_blog_id = int(blog_id)
                if any(blog.id == request_blog_id for blog in user_blogs):
                    create_post_form.blog_id.data = request_blog_id
            except ValueError:
                pass

    if create_post_form.validate_on_submit():
        selected_blog_id = create_post_form.blog_id.data
        if not any(blog.id == selected_blog_id for blog in user_blogs):
            flash("Invalid blog selected.", "danger")
            return redirect(url_for("posts.create_post"))

        post = Post(
            blog_id=selected_blog_id,
            user_id=current_user.id,
            title=create_post_form.title.data,
            content=create_post_form.content.data,
        )
        post.add_post_to_db()
        flash(f"Post '{post.title}' published successfully!", "success")
        return redirect(url_for("profile.profile", username=current_user.username))

    return render_template(
        "create_post.html",
        form=create_post_form,
        blogs=user_blogs,
    )


@post_bp.route("/post/<int:post_id>", methods=["GET"])
def view_post(post_id: int) -> str | tuple[str, int]:
    post = Post.get_post_by_id(post_id=post_id)
    if not post:
        logger.warning(f"Post Route: Post with ID={post_id} not found, rendering 404")
        return render_template("404.html"), 404

    is_author = current_user.is_authenticated and current_user.id == post.user_id
    return render_template(
        "post_detail.html",
        post=post,
        is_author=is_author,
    )


@post_bp.route("/post/<int:post_id>/delete", methods=["POST"])
@login_required
def delete_post(post_id: int) -> Response | tuple[str, int]:
    post = Post.get_post_by_id(post_id=post_id)
    if not post:
        return render_template("404.html"), 404

    if post.user_id != current_user.id:
        return render_template("403.html"), 403

    post_title = post.title
    post.delete_post_from_db()
    flash(f"Post '{post_title}' deleted successfully.", "success")
    return redirect(url_for("profile.profile", username=current_user.username))
