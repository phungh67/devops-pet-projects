from ..extenisions import db

# Association table for Many-to-Many
# RequirementSet <-> Document
requirement_documents_association = db.Table('requirement_documents',
    db.Column('requirement_set_id', db.Integer, db.ForeignKey('requirement_sets.id'), primary_key=True),
    db.Column('document_id', db.Integer, db.ForeignKey('documents.id'), primary_key=True)
)

class Document(db.Model):
    """
    Lookup table for required documents.
    (e.g., "Statement of Purpose", "CV", "Transcript of Records")
    """
    __tablename__ = 'documents'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=True, nullable=False)
    description = db.Column(db.Text, nullable=True)
    
    # This relationship links Documents back to the sets they are part of
    requirement_sets = db.relationship(
        'RequirementSet', 
        secondary=requirement_documents_association,
        back_populates='documents'
    )

    def __repr__(self):
        return f'<Document {self.name}>'

class RequirementSet(db.Model):
    """
    A set of requirements for a program.
    A program can have multiple sets (e.g., for EU vs. non-EU).
    """
    __tablename__ = 'requirement_sets'
    id = db.Column(db.Integer, primary_key=True)
    
    # Name for this set, e.g., "Non-EU Students"
    name = db.Column(db.String(150), nullable=False, default="Standard Requirements")
    
    # Foreign Key for Program
    program_id = db.Column(db.Integer, db.ForeignKey('programs.id'), nullable=False)
    
    # --- Specific Requirement Fields ---
    # (e.g., "Bachelor's", "Master's")
    degree_type_required = db.Column(db.String(100), nullable=True) 
    
    # (e.g., "Engineering", "Researcher")
    career_type = db.Column(db.String(100), nullable=True)
    years_experience_required = db.Column(db.Integer, default=0)
    
    # General description field
    description = db.Column(db.Text, nullable=True)


    # Relationships
    # This links a RequirementSet back to its parent Program
    program = db.relationship('Program', back_populates='requirement_sets')
    
    # This links a RequirementSet to all the Documents it requires
    documents = db.relationship(
        'Document', 
        secondary=requirement_documents_association,
        back_populates='requirement_sets',
        lazy='dynamic'
    )

    def __repr__(self):
        return f'<RequirementSet {self.name} for Program {self.program_id}>'

