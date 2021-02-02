from . import db
import datetime


class Entry(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(80), nullable=False)
    body = db.Column(db.Text, nullable=False)
    pub_date = db.Column(db.DateTime, nullable=False, default=datetime.datetime.utcnow)
    is_published = db.Column(db.Boolean, default=False)


"""
class Contacts(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(15), nullable=False)
    surname = db.Column(db.String(15), nullable=False)
    email = db.Column(db.String(15), nullable=True)
    title = db.Column(db.Integer, nullable=True)
    content = db.Column(db.String(400), nullable=False)
    date_created = db.Column(db.DateTime, default=datetime.datetime.utcnow)

    def __init__(self, name, surname, email, title, content):
        self.name = name
        self.surname = surname
        self.email = email
        self.title = title
        self.content = content
"""