from ..extenisions import db

class Country(db.Model):
    """
    Model for a Country.
    One Country -> Many Universities
    """
    __tablename__ = "countries"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=True, nullable=False)
    # e.g., 'GE', 'SE', 'HU'
    country_code = db.Column(db.String(10), unique=True, nullable=True) 
    
    # Relationship
    universities = db.relationship("University", back_populates="country", cascade="all, delete-orphan")

    def __repr__(self):
        return f'<Country {self.name}>'

class University(db.Model):
    """
    Model for a University.
    Many Universities -> One Country
    One University -> Many Programs
    """
    __tablename__ = "universities"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), nullable=False)
    
    # Foreign Key for Country
    country_id = db.Column(db.Integer, db.ForeignKey("countries.id"), nullable=False)
    
    # Relationships
    country = db.relationship("Country", back_populates="universities")
    programs = db.relationship("Program", back_populates="university", cascade="all, delete-orphan")

    def __repr__(self):
        return f'<University {self.name}>'
