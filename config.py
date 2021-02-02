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
    SENDGRID_API_KEY = os.environ.get("SENDGRID_API_KEY")
    MAIL_SERVER = "smtp.sendgrid.net"
    MAIL_PORT = 465
    MAIL_USERNAME = os.environ.get("MAIL_USERNAME")
    MAIL_PASSWORD = os.environ.get("MAIL_PASSWORD")
    MAIL_DEFAULT_SENDER = os.environ.get("MAIL_DEFAULT_SENDER")
    MAIL_DEFAULT_RECEIVER = os.environ.get("MAIL_DEFAULT_RECEIVER")
    MAIL_USE_SSL = True
    EMAIL_USE_TLS = True


class ProductionConfig(Config):
    DEVELOPMENT = False
    DEBUG = False
