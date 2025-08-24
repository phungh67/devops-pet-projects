# app/models/bookmark.py

from datetime import datetime
from ..extenisions import db


class Bookmark(db.Model):
    __tablename__ = "bookmarks"

    id = db.Column(db.Integer, primary_key=True)
    
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    event_id = db.Column(db.Integer, db.ForeignKey("events.id"), nullable=False)
    
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    # Relationships
    user = db.relationship("User", back_populates="bookmarks")
    event = db.relationship("Event", back_populates="bookmarks")

    def __repr__(self):
        return f"<Bookmark user_id={self.user_id}, event_id={self.event_id}>"
