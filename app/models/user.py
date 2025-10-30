# app/models/user.py

from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from ..extenisions import db, login_manager


class User(UserMixin, db.Model):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(256), nullable=False)

    # --- MODIFIED: Made these nullable=True ---
    # Admin users don't need to provide this info.
    degree = db.Column(db.String(50), nullable=True)
    school = db.Column(db.String(200), nullable=True)
    cpa = db.Column(db.Float, nullable=True)
    # --- END MODIFICATION ---
    
    ranking = db.Column(db.Float, nullable=True)   # percentile or relative score
    study_field = db.Column(db.String(120), nullable=True)

    country_origin = db.Column(db.String(100), nullable=True)
    preferred_destination = db.Column(db.String(100), nullable=True)

    role = db.Column(db.Enum("student", "admin", name="role_types"), default="student", nullable=False)

    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    bookmarks = db.relationship("Bookmark", back_populates="user", cascade="all, delete-orphan")

    # inside User class
    blog_posts = db.relationship("BlogPost", back_populates="author", cascade="all, delete-orphan")

    # Password helpers
    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

