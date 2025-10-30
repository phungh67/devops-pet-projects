from datetime import date, datetime, timedelta
from app import create_app, db

# --- 1. IMPORT ALL NEW MODELS ---
from app.models.user import User
from app.models.blogpost import BlogPost
from app.models.university import Country, University
from app.models.programs import Program
from app.models.requirement import Document, RequirementSet
from app.models.tag import Tag


def seed(config_name="dev"):  # Allow passing in a config name
    app = create_app(config_name)  # Use the config
    with app.app_context():
        db.drop_all()
        db.create_all()

        # --- Users ---
        admin = User(
            name="Admin User", email="admin@example.com", degree="PhD",
            school="Example University", cpa=4.0, study_field="Computer Science",
            country_origin="Germany", role="admin",
        )
        admin.set_password("admin123")
        student = User(
            name="Student User", email="student@example.com", degree="Bachelor",
            school="Some Uni", cpa=3.6, study_field="Physics",
            country_origin="France", role="student",
        )
        student.set_password("student123")
        db.session.add_all([admin, student])
        db.session.commit()

        # --- Blog Posts & Tags ---
        tag_s = Tag(name="scholarships")
        tag_e = Tag(name="eu")
        tag_g = Tag(name="germany")
        # --- FIX: 'nameT' was a typo, changed to 'name' ---
        tag_gu = Tag(name="guide") 
        db.session.add_all([tag_s, tag_e, tag_g, tag_gu])

        b1 = BlogPost(
            title="How to Apply for EU Scholarships", content="Step-by-step guide...",
            author_id=admin.id, post_type=2, tags=[tag_s, tag_e, tag_gu]
        )
        b2 = BlogPost(
            title="Top 5 Universities in Germany", content="An overview of the best...",
            author_id=admin.id, post_type=1, tags=[tag_s, tag_g]
        )
        db.session.add_all([b1, b2])
        db.session.commit()
        
        # --- NEW: COUNTRIES & UNIVERSITIES ---
        c_de = Country(name="Germany", country_code="DE")
        c_eu = Country(name="European Union", country_code="EU")
        db.session.add_all([c_de, c_eu])
        db.session.commit()

        u_tu_berlin = University(name="Technische Universität Berlin", country=c_de)
        u_various_eu = University(name="Various EU Universities", country=c_eu)
        db.session.add_all([u_tu_berlin, u_various_eu])
        db.session.commit()

        # --- NEW: REQUIRED DOCUMENTS (Lookup Table) ---
        doc_lor = Document(name="Letter of Recommendation")
        doc_sop = Document(name="Statement of Purpose")
        doc_cv = Document(name="Curriculum Vitae (CV)")
        doc_transcripts = Document(name="Transcript of Records")
        db.session.add_all([doc_lor, doc_sop, doc_cv, doc_transcripts])
        db.session.commit()

        # --- PROGRAMS (replaces Events) ---
        p1 = Program(
            title="Master Scholarship at TU Berlin",
            program_type="single_program",
            university=u_tu_berlin, # Link to university
            degree_level="Master",
            start_date=date.today() + timedelta(days=1),
            deadline=date.today() + timedelta(days=30),
            description="Full scholarship for international students.",
            source_url="https://www.tu-berlin.de/scholarship",
        )
        p2 = Program(
            title="Erasmus Mundus Joint Master",
            program_type="scholarship", # General scholarship
            university=u_various_eu, # Link to "Various"
            degree_level="Master",
            start_date=date.today() + timedelta(days=15),
            deadline=date.today() + timedelta(days=60),
            description="Erasmus Mundus funded joint master program.",
            source_url="https://erasmus-plus.ec.europa.eu/",
        )
        db.session.add_all([p1, p2])
        db.session.commit()

        # --- NEW: REQUIREMENT SETS ---
        # Create a requirement set for the TU Berlin program
        req_set_p1 = RequirementSet(
            name="Standard Application",
            program=p1, # Link to Program 1
            degree_type_required="Bachelor's",
            career_type="Engineering",
            years_experience_required=0,
            documents=[doc_lor, doc_sop, doc_cv, doc_transcripts] # Link documents
        )
        
        # Create a requirement set for the Erasmus program
        req_set_p2 = RequirementSet(
            name="Erasmus Standard",
            program=p2, # Link to Program 2
            degree_type_required="Bachelor's",
            career_type="Researcher",
            documents=[doc_lor, doc_sop, doc_cv] # Maybe no transcript?
        )
        db.session.add_all([req_set_p1, req_set_p2])
        db.session.commit()
        
        print(f"✅ Database seeded successfully for '{config_name}'!")


if __name__ == "__main__":
    seed()

