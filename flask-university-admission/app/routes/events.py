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
            "source_url": e.source_url,
            "extendedProps": {
                "university": e.university,
                "country": e.country,
                "degree_level": e.degree_level,
                "description": e.description,
            }
        }
        for e in events
    ])


# Public: Calendar HTML page
@events_bp.route("/", methods=["GET"])
def calendar_view():
    events = Event.query.order_by(Event.deadline).all()
    return render_template("events/calendar.html", events=events)
