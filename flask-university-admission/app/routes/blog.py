# app/routes/blog.py

import markdown
from flask import Blueprint, render_template, jsonify, redirect, url_for, flash, request
from flask_login import login_required, current_user
from app.extenisions import db
from app.models.blogpost import BlogPost

import os
from werkzeug.utils import secure_filename

UPLOAD_FOLDER = 'app/static/uploads'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

blog_bp = Blueprint("blog", __name__, url_prefix="/blog")


# --The list blog by JSON API
# Public: JSON API
@blog_bp.route("/api", methods=["GET"])
def list_posts_json():
    posts = BlogPost.query.order_by(BlogPost.created_at.desc()).all()
    return jsonify([
        {
            "id": p.id,
            "title": p.title,
            "content": p.content,
            "author_id": p.author_id,
            "created_at": p.created_at.strftime("%Y-%m-%d %H:%M"),
        }
        for p in posts
    ])

# Public: HTML page
@blog_bp.route("/", methods=["GET"])
def blog_list_view():
    posts = BlogPost.query.order_by(BlogPost.created_at.desc()).all()
    return render_template("blog/list.html", posts=posts)

# @blog_bp.route("/", methods=["GET"])
# def list_posts():
#     posts = BlogPost.query.order_by(BlogPost.created_at.desc()).all()
#     return render_template("blog.html", posts=posts)

@blog_bp.route("/<int:post_id>", methods=["GET"])
def view_post(post_id):
    post = BlogPost.query.get_or_404(post_id)
    rendered_content = markdown.markdown(post.content)
    return render_template("blog_post.html", post=post, rendered_content=rendered_content)

# Create post --- normal user
@blog_bp.route("/create", methods=["GET", "POST"])
@login_required
def create_post():
    if request.method == "POST":
        title = request.form.get("title")
        content = request.form.get("content")
        file = request.files.get("image")

        if not title or not content:
            flash("⚠️ Title and content are required", "warning")
            return redirect(url_for("blog.create_post"))
        
        filename = None
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(UPLOAD_FOLDER, filename))

        # Handling post type
        post_type = 1 if current_user.role == "admin" else 2

        new_post = BlogPost(
            title=title,
            content=content,
            author_id=current_user.id,
            post_type=post_type,
            image_path=filename
        )
        db.session.add(new_post)
        db.session.commit()
        flash("✅ Post created!", "success")
        return redirect(url_for("blog.blog_list_view"))
    
    return render_template("blog_create.html")

# Admin only: deleted admin posts
@blog_bp.route("/<int:post_id>/delete", methods=["POST"])
@login_required
def delete_post(post_id):
    post = BlogPost.query.get_or_404(post_id)

    # ✅ Admin can delete any, user only their own
    if current_user.role != "admin" and post.author_id != current_user.id:
        flash("❌ You cannot delete this post.", "danger")
        return redirect(url_for("blog.view_post", post_id=post.id))

    db.session.delete(post)
    db.session.commit()
    flash("✅ Post deleted.", "success")
    return redirect(url_for("blog.blog_list_view"))


