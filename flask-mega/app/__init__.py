from flask import Flask, request
from config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
from flask_mail import Mail
from flask_moment import Moment
from flask_babel import Babel

from app.errors import bp as errors_bp
from app.auth import bp as auth_bp

def get_locale():
    return request.accept_languages.best_match(app.config['LANGUAGES'])

app = Flask(__name__)
app.config.from_object(Config)
app.register_blueprint(errors_bp)
app.register_blueprint(auth_bp, url_prefix='/auth')

db = SQLAlchemy(app)
migrate = Migrate(app, db)
login = LoginManager(app)
login.login_view = 'login'
mail = Mail(app)
moment = Moment(app)
babel = Babel(app, locale_selector=get_locale)

from app import routes, models