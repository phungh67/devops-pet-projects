from datetime import date, datetime, timedelta
from app import create_app, db
from app.models.user import User
from app.models.event import Event
from app.models.blogpost import BlogPost


def seed():
    app = create_app("dev")  # use your dev config
    with app.app_context():
        db.drop_all()
        db.create_all()

        # --- Users ---
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
        admin.set_password("admin123")  # ✅ hash password

        student = User(
            name="Student User",
            email="student@example.com",
            degree="Bachelor",
            school="Some Uni",
            cpa=3.6,
            study_field="Physics",
            country_origin="France",
            role="student",
        )
        student.set_password("student123")  # ✅ hash password

        db.session.add_all([admin, student])
        db.session.commit()

        # --- Events ---
        e1 = Event(
            title="Master Scholarship at TU Berlin",
            university="Technische Universität Berlin",
            country="Germany",
            degree_level="Master",   # ✅ match field name in model
            deadline=date.today() + timedelta(days=30),
            description="Full scholarship for international students.",
            source_url="https://www.tu-berlin.de/scholarship",
        )

        e2 = Event(
            title="Erasmus Mundus Joint Master",
            university="Various Universities",
            country="EU",
            degree_level="Master",
            deadline=date.today() + timedelta(days=60),
            description="Erasmus Mundus funded joint master program.",
            source_url="https://erasmus-plus.ec.europa.eu/",
        )

        db.session.add_all([e1, e2])
        db.session.commit()

        # --- Blog Posts ---
        b1 = BlogPost(
            title="How to Apply for EU Scholarships",
            content="Step-by-step guide for EU-based scholarships.",
            author_id=admin.id,
            post_type=2
        )

        b2 = BlogPost(
            title="Top 5 Universities in Germany",
            content="An overview of the best German universities for Masters.",
            author_id=admin.id,
            post_type=1
        )

        db.session.add_all([b1, b2])
        db.session.commit()

        print("✅ Database seeded successfully!")


if __name__ == "__main__":
    seed()
