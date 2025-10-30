import os
from flask import Flask
# --- 1. IMPORT THE CONFIG DICTIONARY ---
from .config import config_by_name
from .extenisions import db, migrate, login_manager

# --- 2. IMPORT YOUR BLUEPRINTS ---
from app.routes.events import events_bp
from app.routes.blog import blog_bp
from app.routes.home import home_bp
from app.routes.auth import auth_bp
# from .views import register_blueprints

def create_app(config_name: str | None = None):
    """Application factory for ScholarTrack
    
    Keyword arguments:
    argument -- 
        config_name ( str | None ): Enviroment name to be passed (dev, prod, test),
                                    defaults to FLASK_ENV or 'dev'
    Return: A Flask application
    """ 

    # Dynamically pick and overdrive enviroment
    config_name = config_name or os.getenv("FLASK_ENV", "dev")

    app = Flask(__name__)
    # --- 3. DYNAMICALLY LOAD CONFIG (FIXED) ---
    app.config.from_object(config_by_name[config_name])

    # Initialize extensions
    db.init_app(app)
    migrate.init_app(app, db)
    login_manager.init_app(app)

    # --- 4. IMPORT MODELS (AFTER DB INIT) ---
    # This will run the 'app/models/__init__.py' file
    # which correctly imports all your models in order.
    with app.app_context():
        from . import models

    # Register blueprints
    app.register_blueprint(events_bp)
    app.register_blueprint(blog_bp)
    app.register_blueprint(home_bp)
    app.register_blueprint(auth_bp)

    return app
