# app/models/event.py

from datetime import datetime
from ..extenisions import db


class Event(db.Model):
    __tablename__ = "events"

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    university = db.Column(db.String(200), nullable=False)
    country = db.Column(db.String(100), nullable=False)

    degree_level = db.Column(db.String(50), nullable=False)

    start_date = db.Column(db.Date, nullable=False)

    deadline = db.Column(db.Date, nullable=False)
    description = db.Column(db.Text, nullable=True)
    source_url = db.Column(db.String(300), nullable=True)

    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    bookmarks = db.relationship("Bookmark", back_populates="event", cascade="all, delete-orphan")

    def __repr__(self):
        return f"<Event {self.title} @ {self.university}>"
