from datetime import datetime
from ..extenisions import db

class Program(db.Model):
    """
    Model for a specific Program or a general Scholarship.
    This REPLACES the old 'Event' model.
    Many Programs -> One University
    One Program -> Many Requirement Sets
    """
    __tablename__ = "programs"

    id = db.Column(db.Integer, primary_key=True)
    
    # To distinguish "MSc at KTH" from "Erasmus Scholarship"
    program_type = db.Column(
        db.Enum('single_program', 'scholarship', name='program_types'),
        nullable=False, 
        default='single_program'
    )
    
    title = db.Column(db.String(200), nullable=False)
    degree_level = db.Column(db.String(50), nullable=False)
    description = db.Column(db.Text, nullable=True)
    source_url = db.Column(db.String(300), nullable=True)

    # Deadlines
    start_date = db.Column(db.Date, nullable=True) # Application open date
    deadline = db.Column(db.Date, nullable=False) # Application close date

    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Foreign Key for University
    # Nullable=True because a general scholarship (like Erasmus)
    # isn't tied to one single university.
    university_id = db.Column(db.Integer, db.ForeignKey("universities.id"), nullable=True) 
    
    # Relationships
    university = db.relationship("University", back_populates="programs")
    bookmarks = db.relationship("Bookmark", back_populates="program", cascade="all, delete-orphan")
    requirement_sets = db.relationship('RequirementSet', back_populates='program', cascade="all, delete-orphan")

    def __repr__(self):
        if self.university:
            return f"<Program {self.title} @ {self.university.name}>"
        return f"<Program {self.title} (Scholarship)>"
