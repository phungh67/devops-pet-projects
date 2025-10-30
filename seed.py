from datetime import date
from app import create_app, db

# Import all our new models in the correct order
from app.models.user import User
from app.models.university import Country, University
from app.models.programs import Program
from app.models.requirement import Document, RequirementSet
from app.models.blogpost import BlogPost
from app.models.tag import Tag


def seed(config_name="dev"):  # Allow passing in a config name
    app = create_app(config_name)  # Use the config
    with app.app_context():
        print("Dropping and recreating database...")
        db.drop_all()
        db.create_all()

        # --- 1. Create Users ---
        admin = User(
            name="Admin User",
            email="admin@example.com",
            degree="PhD",
            school="Example University",
            cpa=4.0,
            study_field="Computer Science",
            country_origin="Germany",
            role="admin",
        )
        admin.set_password("admin123")

        student = User(
            name="Student User",
            email="student@example.com",
            degree="Bachelor",
            school="Some Uni",
            cpa=3.6,
            study_field="Cybersecurity",
            country_origin="Sweden",
            role="student",
        )
        student.set_password("student123")
        
        db.session.add_all([admin, student])

        # --- 2. Create Countries ---
        c_sweden = Country(name="Sweden", country_code="SE")
        c_germany = Country(name="Germany", country_code="DE")
        c_eu = Country(name="European Union", country_code="EU")
        
        db.session.add_all([c_sweden, c_germany, c_eu])

        # --- 3. Create Universities ---
        u_kth = University(
            name="KTH Royal Institute of Technology", 
            country=c_sweden
        )
        u_chalmers = University(
            name="Chalmers University of Technology", 
            country=c_sweden
        )
        u_various_eu = University(
            name="Various Universities",
            country=c_eu
        )
        
        db.session.add_all([u_kth, u_chalmers, u_various_eu])

        # --- 4. Create Document Lookup Table ---
        doc_lor = Document(name="Letter of Recommendation")
        doc_sop = Document(name="Statement of Purpose")
        doc_transcript = Document(name="Academic Transcripts")
        doc_degree = Document(name="Degree Certificate")
        doc_cv = Document(name="Curriculum Vitae (CV)")
        doc_english = Document(name="English Proficiency Test (IELTS/TOEFL)")
        
        db.session.add_all([doc_lor, doc_sop, doc_transcript, doc_degree, doc_cv, doc_english])
        
        # --- 5. Create Tags for Blog ---
        tag_scholarships = Tag(name="scholarships")
        tag_eu = Tag(name="eu")
        tag_germany = Tag(name="germany")
        tag_guide = Tag(name="guide")
        
        db.session.add_all([tag_scholarships, tag_eu, tag_germany, tag_guide])

        # Commit all the lookup tables and users
        print("Committing Users, Countries, Unis, Docs, and Tags...")
        db.session.commit()

        # --- 6. Create Programs ---
        p_kth_cyber = Program(
            title="Master's in Cybersecurity",
            program_type="single_program",
            university=u_kth,
            degree_level="Master",
            deadline=date(2025, 1, 15),
            start_date=date(2025, 8, 28),
            description="Master's programme in Cybersecurity at KTH.",
            source_url="https://www.kth.se/en/studies/master/cybersecurity"
        )
        
        p_chalmers_cyber = Program(
            title="Computer Systems and Cybersecurity, MSc",
            program_type="single_program",
            university=u_chalmers,
            degree_level="Master",
            deadline=date(2025, 1, 15),
            start_date=date(2025, 8, 28),
            description="Master's programme at Chalmers.",
            source_url="https://www.chalmers.se/en/education/find-masters-programme/computer-systems-and-cybersecurity-msc/"
        )
        
        p_erasmus = Program(
            title="Erasmus Mundus Joint Master",
            program_type="scholarship",
            university=u_various_eu,
            degree_level="Master",
            deadline=date(2025, 2, 1),
            start_date=date(2025, 9, 1),
            description="General Erasmus scholarship program.",
            source_url="https://erasmus-plus.ec.europa.eu/"
        )

        db.session.add_all([p_kth_cyber, p_chalmers_cyber, p_erasmus])

        # --- 7. Create Requirements for Programs ---
        
        # KTH Requirements
        req_kth_degree = RequirementSet(program=p_kth_cyber, requirement_type="degree", description="Bachelor's degree in Computer Science or equivalent.")
        req_kth_docs = RequirementSet(program=p_kth_cyber, requirement_type="documents", description="Standard application documents via University Admissions Sweden.")
        req_kth_docs.documents.extend([doc_sop, doc_transcript, doc_degree, doc_cv, doc_english])
        
        # Chalmers Requirements
        req_chalmers_degree = RequirementSet(program=p_chalmers_cyber, requirement_type="degree", description="Bachelor's degree in CS, Software Eng, or equivalent.")
        req_chalmers_docs = RequirementSet(program=p_chalmers_cyber, requirement_type="documents", description="Standard documents + 2 LORs.")
        req_chalmers_docs.documents.extend([doc_lor, doc_sop, doc_transcript, doc_degree, doc_cv, doc_english])
        
        # Erasmus Requirements
        req_erasmus_docs = RequirementSet(program=p_erasmus, requirement_type="documents", description="Varies by program, but generally includes these.")
        req_erasmus_docs.documents.extend([doc_lor, doc_sop, doc_cv, doc_transcript])
        
        db.session.add_all([req_kth_degree, req_kth_docs, req_chalmers_degree, req_chalmers_docs, req_erasmus_docs])

        # --- 8. Create Blog Posts ---
        b1 = BlogPost(
            title="How to Apply for EU Scholarships",
            content="Step-by-step guide for EU-based scholarships.",
            author_id=admin.id,
            post_type=2,
            tags=[tag_scholarships, tag_eu, tag_guide]
        )

        b2 = BlogPost(
            title="KTH vs Chalmers: Cybersecurity",
            content="An overview of the two best cybersecurity master's in Sweden.",
            author_id=admin.id,
            post_type=1,
            tags=[tag_scholarships, tag_germany] # Whoops, should be sweden, but we'll use 'germany' tag for testing
        )

        db.session.add_all([b1, b2])

        # --- Final Commit ---
        print("Committing Programs, Requirements, and Blog Posts...")
        db.session.commit()

        print(f"✅ Database seeded successfully for '{config_name}'!")


if __name__ == "__main__":
    seed()

