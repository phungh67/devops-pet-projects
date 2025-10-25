# app/routes/events.py

from flask import Blueprint, render_template, jsonify
from app.models.event import Event
from ..extenisions import db

events_bp = Blueprint("events", __name__, url_prefix="/events")


# Public: JSON endpoint (for API/JS frontend use)
@events_bp.route("/api", methods=["GET"])
def list_events_json():
    events = Event.query.all()
    return jsonify([
        {
            "id": e.id,
            "title": e.title,
            "start": e.deadline.strftime("%Y-%m-%d"),
            # "source_url": e.source_url,
            "extendedProps": {
                "university": e.university,
                "country": e.country,
                "degree_level": e.degree_level,
                "description": e.description,
                "source_url": e.source_url,
            }
        }
        for e in events
    ])


# Public: Calendar HTML page
@events_bp.route("/", methods=["GET"])
def calendar_view():
    events = Event.query.order_by(Event.deadline).all()
    return render_template("events/calendar.html", events=events)

@events_bp.route("/api/gantt", methods=["GET"])
def list_events_gantt_json():
    events = Event.query.all()
    
    # Format data specifically for Frappe Gantt
    tasks = [
        {
            "id": str(e.id),
            "name": e.title,
            "start": e.start_date.strftime("%Y-%m-%d"),
            "end": e.deadline.strftime("%Y-%m-%d"),
            "progress": 50,  # You can make this dynamic later
            "source_url": e.source_url
        }
        for e in events
    ]
    return jsonify(tasks)

# In: app/routes/events.py

@events_bp.route("/gantt", methods=["GET"])
def gantt_view():
    return render_template("events/gantt.html")
