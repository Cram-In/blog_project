from blog.models import Entry, db
from blog.forms import EntryForm


def new_entry(form):
    entry = Entry(title=form.title.data, body=form.body.data, is_published=form.is_published.data)
    db.session.add(entry)
    db.session.commit()