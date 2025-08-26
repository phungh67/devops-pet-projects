# app/routes/blog.py

from flask import Blueprint, render_template, jsonify
from app.models.blogpost import BlogPost

blog_bp = Blueprint("blog", __name__, url_prefix="/blog")


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
