from flask import Flask, request, render_template, redirect, flash, session, url_for
from blog import app
from blog.models import Entry, db, Contacts
from blog.forms import EntryForm, LoginForm, ContactForm
import functools
import os
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail


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
        is_published = form.is_published.data
        if is_published == True:
            entry = Entry(title=form.title.data, body=form.body.data, is_published=form.is_published.data)
            db.session.add(entry)
            db.session.commit()
            flash("Your Post has been published!", "success")
            return redirect("/")
        elif is_published == False:
            entry = Entry(title=form.title.data, body=form.body.data, is_published=form.is_published.data)
            db.session.add(entry)
            db.session.commit()
            flash("Post created and saved in Drafts", "info")
            return redirect("/")
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
            flash("Your Post has been updated!", "info")
            return redirect("/")
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
    return redirect("/drafts/")


@app.route("/contact/", methods=["GET", "POST"])
def contact():

    form = ContactForm()
    error = None
    if request.method == "POST":

        if form.validate_on_submit():

            email = request.form["email"]
            title = request.form["title"]
            name = request.form["name"]
            surname = request.form["surname"]
            content = request.form["content"]

            message = Mail(
                from_email=email,
                to_emails=os.environ.get("MAIL_DEFAULT_SENDER"),
                subject=title,
                html_content="<strong><p>Message from {name} {surname}</p><br><p>{content}</p></strong>",
            )
            try:
                sg = SendGridAPIClient(os.environ.get("SENDGRID_API_KEY"))
                response = sg.send(message)

                print(response.status_code)
                print(response.body)
                print(response.headers)

                flash("Message send!", "success")
                return redirect("/contact/")
            except Exception as e:
                print(f"error", e.body)

    return render_template("/contact.html")