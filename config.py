class Config(object):
    DEBUG = True
    DEVELOPMENT = True
    FLASK_HTPASSWD_PATH = "/secret/.htpasswd"
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_DATABASE_URI = "sqlite:///posts.db"
    SECRET_KEY = "do-i-really-need-this"


class ProductionConfig(Config):
    DEVELOPMENT = False
    DEBUG = False
