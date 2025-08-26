import os
from flask import Flask
from .config import DevConfig
from .extenisions import db, migrate, login_manager
from .models import user, bookmark, event, blogpost
from app.routes.events import events_bp
from app.routes.blog import blog_bp
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
    app.config.from_object(DevConfig)

    # Initialize extensions
    db.init_app(app)
    migrate.init_app(app, db)
    login_manager.init_app(app)

    # Register blueprints
    app.register_blueprint(events_bp)
    app.register_blueprint(blog_bp)

    return app
    