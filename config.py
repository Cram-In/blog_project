import os


class Config(object):
    DEBUG = True
    DEVELOPMENT = True
    FLASK_HTPASSWD_PATH = "/secret/.htpasswd"
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_DATABASE_URI = "sqlite:///posts.db"
    SECRET_KEY = "do-i-really-need-this"
    ADMIN_USERNAME = os.environ.get("ADMIN_USERNAME", "")
    ADMIN_PASSWORD = os.environ.get("ADMIN_PASSWORD", "")


class ProductionConfig(Config):
    DEVELOPMENT = False
    DEBUG = False
