# app/models/bookmark.py

from datetime import datetime
from ..extenisions import db
from . import programs


class Bookmark(db.Model):
# ... existing code ...
    id = db.Column(db.Integer, primary_key=True)
    
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    # --- CHANGE ---
    # Renamed from event_id to program_id
    program_id = db.Column(db.Integer, db.ForeignKey("programs.id"), nullable=False)
    # --- END CHANGE ---
    
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    # Relationships
    user = db.relationship("User", back_populates="bookmarks")
    # --- CHANGE ---
    program = db.relationship("Program", back_populates="bookmarks")
    # --- END CHANGE ---

    def __repr__(self):
        return f"<Bookmark user_id={self.user_id}, program_id={self.program_id}>"
