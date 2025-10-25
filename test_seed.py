# In: test_seed.py

import pytest
from app import create_app, db
from app.models.user import User
from app.models.event import Event
from app.models.blogpost import BlogPost
from seed import seed  # Import our modified seed function

@pytest.fixture(scope="module")
def seeded_db():
    """
    Pytest fixture to set up a test app and seed a test database.
    This runs ONCE for all tests in this file.
    """
    # 1. Create an app with the 'test' configuration
    app = create_app("test") 
    
    with app.app_context():
        # 2. Run the seeder function, telling it to use the 'test' config
        seed(config_name="test")
        
        # 3. Make the app available to the tests
        yield app

    # 4. Teardown: drop all tables after tests are done
    with app.app_context():
        db.drop_all()

# --- Tests ---

def test_user_creation_count(seeded_db):
    """Test that the correct number of users were created."""
    assert User.query.count() == 2
    
def test_admin_user_details(seeded_db):
    """Test the details and password of the admin user."""
    admin = User.query.filter_by(email="admin@example.com").first()
    assert admin is not None
    assert admin.name == "Admin User"
    assert admin.role == "admin"
    assert admin.check_password("admin123") == True
    assert admin.check_password("wrongpassword") == False

def test_student_user_details(seeded_db):
    """Test the details of the student user."""
    student = User.query.filter_by(role="student").first()
    assert student is not None
    assert student.name == "Student User"
    assert student.check_password("student123") == True

def test_event_creation_count(seeded_db):
    """Test that the correct number of events were created."""
    assert Event.query.count() == 2

def test_event_details(seeded_db):
    """Test the details of a created event."""
    event = Event.query.filter_by(title="Master Scholarship at TU Berlin").first()
    assert event is not None
    assert event.country == "Germany"
    assert event.source_url == "https://www.tu-berlin.de/scholarship"
    assert event.start_date is not None # Check that start_date was added

def test_blogpost_creation_count(seeded_db):
    """Test that the correct number of blog posts were created."""
    assert BlogPost.query.count() == 2

def test_blogpost_author_relationship(seeded_db):
    """Test that blog posts are correctly linked to their author."""
    # Get the admin user
    admin = User.query.filter_by(email="admin@example.com").first()
    
    # Get a post that should be by the admin
    post = BlogPost.query.filter_by(title="Top 5 Universities in Germany").first()
    
    assert post is not None
    assert admin is not None
    
    # Test the relationship
    assert post.author_id == admin.id
    assert post.author == admin
    assert post.post_type == 1 # Check post_type