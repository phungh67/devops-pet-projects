# app/routes/events.py

from flask import Blueprint, render_template, jsonify
# --- 1. IMPORT PROGRAM (replaces Event) ---
from app.models.programs import Program
from ..extenisions import db

events_bp = Blueprint("events", __name__, url_prefix="/events")


# Public: JSON endpoint (for API/JS frontend use)
@events_bp.route("/api", methods=["GET"])
def list_events_json():
    # --- 2. QUERY PROGRAM (replaces Event) ---
    programs = Program.query.all()
    
    return jsonify([
        {
            "id": p.id,
            "title": p.title,
            "start": p.deadline.strftime("%Y-%m-%d"),
            "extendedProps": {
                # 3. Access university/country via relationships
                "university": p.university.name if p.university else "N/A (Scholarship)",
                "country": p.university.country.name if p.university and p.university.country else "Various",
                "degree_level": p.degree_level,
                "description": p.description,
                "source_url": p.source_url,
            }
        }
        for p in programs
    ])


# Public: Calendar HTML page
@events_bp.route("/", methods=["GET"])
def calendar_view():
    # --- 4. QUERY PROGRAM (replaces Event) ---
    programs = Program.query.order_by(Program.deadline).all()
    return render_template("events/calendar.html", events=programs)

@events_bp.route("/api/gantt", methods=["GET"])
def list_events_gantt_json():
    # --- 5. QUERY PROGRAM (replaces Event) ---
    programs = Program.query.all()
    
    # Format data specifically for Frappe Gantt
    tasks = [
        {
            "id": str(p.id),
            "name": p.title,
            # Handle possible null start_date
            "start": p.start_date.strftime("%Y-%m-%d") if p.start_date else p.deadline.strftime("%Y-%m-%d"),
            "end": p.deadline.strftime("%Y-%m-%d"),
            "progress": 50,
            "source_url": p.source_url
        }
        for p in programs
    ]
    return jsonify(tasks)

# In: app/routes/events.py

@events_bp.route("/gantt", methods=["GET"])
def gantt_view():
    return render_template("events/gantt.html")

