from flask import Blueprint, render_template
from app.models.event import Event
from app.models.blogpost import BlogPost

home_bp = Blueprint("home", __name__)

@home_bp.route("/")
def home():
    events = Event.query.order_by(Event.deadline.asc()).limit(5).all()
    posts = BlogPost.query.order_by(BlogPost.created_at.desc()).limit(3).all()
    return render_template("home.html", events=events, posts=posts)