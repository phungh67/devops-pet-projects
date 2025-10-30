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
        # MODIFIED: Admin user is minimal
        admin = User(
            name="Admin User",
            email="admin@example.com",
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
        u_tu_berlin = University(
            name="TU Berlin",
            country=c_germany
        )
        u_various_eu = University(
            name="Various Universities",
            country=c_eu
        )
        
        db.session.add_all([u_kth, u_chalmers, u_tu_berlin, u_various_eu])

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
        tag_sweden = Tag(name="sweden") # <-- ADDED SWEDEN TAG
        
        db.session.add_all([tag_scholarships, tag_eu, tag_germany, tag_guide, tag_sweden])

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
        
        p_tu_berlin = Program(
            title="Master Scholarship at TU Berlin",
            program_type="scholarship",
            university=u_tu_berlin,
            degree_level="Master",
            deadline=date(2024, 11, 30),
            start_date=date(2024, 10, 1),
            description="Scholarship for CS at TU Berlin.",
            source_url="https." # Placeholder
        )

        db.session.add_all([p_kth_cyber, p_chalmers_cyber, p_erasmus, p_tu_berlin])

        # --- 7. Create Requirements for Programs ---
        
        # MODIFIED: Combined into ONE RequirementSet per program
        req_kth = RequirementSet(
            name="KTH Cybersecurity Requirements",
            program=p_kth_cyber, 
            degree_type_required="Bachelor's in Computer Science",
            career_type="Engineering",
            description="Standard application documents via University Admissions Sweden."
        )
        req_kth.documents.extend([doc_sop, doc_transcript, doc_degree, doc_cv, doc_english])
        
        req_chalmers = RequirementSet(
            name="Chalmers Cybersecurity Requirements",
            program=p_chalmers_cyber, 
            degree_type_required="Bachelor's in CS, Software Eng, or equivalent.",
            career_type="Engineering",
            description="Standard documents + 2 LORs.",
            years_experience_required=0
        )
        req_chalmers.documents.extend([doc_lor, doc_sop, doc_transcript, doc_degree, doc_cv, doc_english])
        
        req_erasmus = RequirementSet(
            name="General Erasmus Requirements",
            program=p_erasmus, 
            degree_type_required="Bachelor's Degree",
            description="Varies by program, but generally includes these."
        )
        req_erasmus.documents.extend([doc_lor, doc_sop, doc_cv, doc_transcript])
        
        req_tu_berlin = RequirementSet(
            name="TU Berlin Scholarship Requirements",
            program=p_tu_berlin,
            degree_type_required="Bachelor's Degree in CS"
        )
        req_tu_berlin.documents.extend([doc_lor, doc_sop, doc_degree])
        
        db.session.add_all([req_kth, req_chalmers, req_erasmus, req_tu_berlin])

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
            tags=[tag_scholarships, tag_sweden] # <-- FIXED "Whoops"
        )

        db.session.add_all([b1, b2])

        # --- Final Commit ---
        print("Committing Programs, Requirements, and Blog Posts...")
        db.session.commit()

        print(f"✅ Database seeded successfully for '{config_name}'!")


if __name__ == "__main__":
    seed()