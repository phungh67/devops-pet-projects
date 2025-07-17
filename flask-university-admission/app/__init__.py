from flask import Flask

def create_app():
    app = Flask(__name__)

    # Register routes
    from .routes.home import home_bp
    # from .routes.scholarships import scholarships_bp
    # from .routes.admissions import admissions_bp
    # from .routes.checklist import checklist_bp

    app.register_blueprint(home_bp)
    # app.register_blueprint(scholarships_bp, url_prefix="/scholarships")
    # app.register_blueprint(admissions_bp, url_prefix="/admissions")
    # app.register_blueprint(checklist_bp, url_prefix="/checklist")

    return app
