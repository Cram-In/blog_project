from flask import Flask, request, render_template, redirect, flash, session, url_for
from blog import app
from blog.models import Entry, db
from blog.forms import EntryForm, LoginForm
import functools


@app.route("/")
def index():
    all_posts = Entry.query.filter_by(is_published=True).order_by(Entry.pub_date.desc())
    return render_template("homepage.html", all_posts=all_posts)


def login_required(view_func):
    @functools.wraps(view_func)
    def check_permissions(*args, **kwargs):
        if session.get("logged_in"):
            return view_func(*args, **kwargs)
        return redirect(url_for("login", next=request.path))

    return check_permissions


@app.route("/post/", methods=["GET", "POST"])
@login_required
def create_entry():
    form = EntryForm()
    errors = None
    if request.method == "POST":
        if form.validate_on_submit():
            entry = Entry(title=form.title.data, body=form.body.data, is_published=form.is_published.data)
            db.session.add(entry)
            db.session.commit()
        else:
            errors = form.errors
    return render_template("entry_form.html", form=form, errors=errors)


@app.route("/edit-post/<int:entry_id>", methods=["GET", "POST"])
@login_required
def edit_entry(entry_id):

    entry = Entry.query.filter_by(id=entry_id).first_or_404()
    form = EntryForm(obj=entry)
    errors = None
    if request.method == "POST":

        if form.validate_on_submit():
            form.populate_obj(entry)
            db.session.commit()

        else:
            errors = form.errors
    return render_template("entry_form.html", form=form, errors=errors)


@app.route("/login/", methods=["GET", "POST"])
def login():
    form = LoginForm()
    errors = None
    next_url = request.args.get("next")
    if request.method == "POST":
        if form.validate_on_submit():
            session["logged_in"] = True
            session.permanent = True  # Use cookie to store session.
            flash("You are now logged in.", "success")
            return redirect("/")
        else:
            errors = form.errors
    return render_template("login_form.html", form=form, errors=errors)


@app.route("/logout/", methods=["GET", "POST"])
def logout():
    if request.method == "POST":
        session.clear()
        flash("You are now logged out.", "success")
    return redirect("/")


@app.route("/drafts/", methods=["GET", "POST"])
def drafts():
    all_drafts = Entry.query.filter_by(is_published=False).order_by(Entry.pub_date.desc())
    return render_template("drafts.html", all_drafts=all_drafts)


@app.route("/delete/<int:entry_id>")
def delete_entry(entry_id):
    entry = Entry.query.get(entry_id)
    errors = None
    if not entry:
        return redirect("/")

    db.session.delete(entry)
    db.session.commit()
    flash("Post Deleted.", "success")
    return redirect("/")


@app.route("/contact/", methods=["GET", "POST"])
def contact():
    return render_template("contact.html")