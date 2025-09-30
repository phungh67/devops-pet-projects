import os

class Config:
    """Base configuration (shared defaults)."""
    SECRET_KEY = os.getenv("SECRET_KEY", "super-secret-key")
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # Default fallback to SQLite if nothing is set
    SQLALCHEMY_DATABASE_URI = os.getenv("DATABASE_URL", "sqlite:///dev.db")


class DevConfig(Config):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = os.getenv(
        "DEV_DATABASE_URL",
        "mysql+pymysql://root:flask-root-pw@127.0.0.1/scholartrack_dev"
    )


class ProdConfig(Config):
    DEBUG = False
    SQLALCHEMY_DATABASE_URI = os.getenv(
        "PROD_DATABASE_URL",
        "mysql+pymysql://user:password@rds.amazonaws.com:3306/scholartrack_prod"
    )


class TestConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = os.getenv(
        "TEST_DATABASE_URL",
        "mysql+pymysql://root:password@localhost:3306/scholartrack_test"
    )


# Map for easy access in app factory
config_by_name = dict(
    dev=DevConfig,
    prod=ProdConfig,
    test=TestConfig,
)
