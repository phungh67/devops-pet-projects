# app/models/blogpost.py

from datetime import datetime
from ..extenisions import db
from .tag import post_tags


class BlogPost(db.Model):
    __tablename__ = "blog_posts"

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    content = db.Column(db.Text, nullable=False)

    author_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)

    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    author = db.relationship("User", back_populates="blog_posts")

    # Authorized post only
    post_type = db.Column(db.Integer, default=2, nullable=False)

    # add new property to allow pictures/images in blog posts
    image_path = db.Column(db.String(255), nullable=True)

    # Relationship with the tag, to sort easier
    tags = db.relationship('Tag', secondary=post_tags,
                            back_populates='posts', lazy='dynamic')
    

    @property
    def is_admin_post(self):
        return self.post_type == 1

    def __repr__(self):
        return f"<BlogPost {self.title}>"
