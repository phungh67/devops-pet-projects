from flask import Blueprint, render_template
# --- 1. IMPORT PROGRAM (replaces Event) ---
from app.models.programs import Program
from app.models.blogpost import BlogPost

home_bp = Blueprint("home", __name__)

@home_bp.route("/")
def home():
    # --- 2. QUERY PROGRAM (replaces Event) ---
    programs = Program.query.order_by(Program.deadline.asc()).limit(5).all()
    posts = BlogPost.query.order_by(BlogPost.created_at.desc()).limit(3).all()
    
    # --- 3. Pass 'programs' to the template ---
    return render_template("home.html", programs=programs, posts=posts)

