# In: app/models/tag.py
from ..extenisions import db

# This is the association table
# It links BlogPost (post_id) to Tag (tag_id)
post_tags = db.Table('post_tags',
    db.Column('post_id', db.Integer, db.ForeignKey('blog_posts.id'), primary_key=True),
    db.Column('tag_id', db.Integer, db.ForeignKey('tags.id'), primary_key=True)
)

class Tag(db.Model):
    __tablename__ = 'tags'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), unique=True, nullable=False)

    # The 'posts' relationship will be defined in the BlogPost model
    posts = db.relationship('BlogPost', secondary=post_tags,
                             back_populates='tags', lazy='dynamic')
    
    def __repr__(self):
        return f'<Tag {self.name}>'