import os


class Config(object):
    DEBUG = os.environ.get("BUG_SET")
    DEVELOPMENT = os.environ.get("DEV_SET")
    FLASK_HTPASSWD_PATH = "/secret/.htpasswd"
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_DATABASE_URI = os.environ.get("DATABASE_URL")
    SECRET_KEY = "do-i-really-need-this"
    ADMIN_USERNAME = os.environ.get("ADMIN_USERNAME", "")
    ADMIN_PASSWORD = os.environ.get("ADMIN_PASSWORD", "")
    SENDGRID_API_KEY = os.environ.get("SENDGRID_API_KEY")
    MAIL_SERVER = os.environ.get("SMTP_MAIL_SERVER")
    MAIL_PORT = os.environ.get("PORT")
    MAIL_USERNAME = os.environ.get("MAIL_USERNAME")
    MAIL_PASSWORD = os.environ.get("MAIL_PASSWORD")
    MAIL_DEFAULT_SENDER = os.environ.get("MAIL_DEFAULT_SENDER")
    MAIL_DEFAULT_RECEIVER = os.environ.get("MAIL_DEFAULT_RECEIVER")
    MAIL_USE_SSL = True
    EMAIL_USE_TLS = True