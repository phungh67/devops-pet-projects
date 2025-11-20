from flask import Blueprint, render_template, redirect, url_for, flash, request, jsonify
from flask_login import login_required, current_user
from app.extenisions import db
from app.models.bookmark import Bookmark
from app.models.programs import Program
from app.models.user import User

dashboard_bp = Blueprint("dashboard", __name__, url_prefix="/dashboard")

@dashboard_bp.route("/") #default page for login user
@login_required
def user_dashboard():
    """
    Main dashboard page. Shows bookmarked programs.
    """
    # allow user to fetch boorkmarked program (highlighted)
    bookmarked_programs = [bookmark.program for bookmark in current_user.bookmarks]
    
    return render_template(
        "dashboard/main.html", 
        user=current_user, 
        programs=bookmarked_programs
    )


@dashboard_bp.route("/profile", methods=["GET", "POST"])
@login_required
def profile(): # allow user to customize thier dashboard, profile
