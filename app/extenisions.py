from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager

# Initialize extensions
db = SQLAlchemy()
migrate = Migrate()
login_manager = LoginManager()

# Default for login view
login_manager.login_view = "auth.login"
login_manager.login_message = "Please login to see this page"