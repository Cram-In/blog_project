from flask import Flask, request, render_template, redirect, flash, session, url_for
from blog import app
from blog.models import Entry, db
from blog.forms import EntryForm, LoginForm, ContactForm
from blog.decorators import login_required
from blog.func import new_entry
import os
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail


@app.route("/")
def index():
    all_posts = Entry.query.filter_by(is_published=True).order_by(Entry.pub_date.desc())
    return render_template("homepage.html", all_posts=all_posts)


@app.route("/post/", methods=["GET", "POST"])
@login_required
def create_entry():
    form = EntryForm()
    errors = None
    if request.method == "POST":
        is_published = form.is_published.data
        if is_published == True:
            new_entry(form)
            flash("Your Post has been published!", "success")
            return redirect("/")
        elif is_published == False:
            new_entry(form)
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
    if request.method == "POST":
        if not form.validate_on_submit():

            email = request.form["email"]
            title = request.form["title"]
            name = request.form["name"]
            surname = request.form["surname"]
            content = request.form["email_content"]

            message = Mail(
                from_email=os.environ.get("MAIL_DEFAULT_SENDER"),
                to_emails=os.environ.get("MAIL_DEFAULT_RECEIVER"),
                subject=f"From {email}. Subject: {title}",
                html_content=f"<strong>Message from: <p>{name} {surname}.</p><p>MESSAGE:</p> <p>{content}</p> </strong>",
            )
            try:
                sg = SendGridAPIClient(os.environ.get("SENDGRID_API_KEY"))
                response = sg.send(message)
                print(response.status_code)
                print(response.body)
                print(response.headers)
                flash("Message Send.", "success")
                return redirect("/contact/")
            except Exception as e:
                print(f"error", e.body)
    return render_template("/contact.html")
