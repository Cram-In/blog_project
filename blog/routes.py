from flask import Flask, request, render_template, redirect, flash
from blog import app
from blog.models import Entry, db
from blog.forms import EntryForm


@app.route("/")
def index():
    all_posts = Entry.query.filter_by(is_published=True).order_by(Entry.pub_date.desc())
    return render_template("homepage.html", all_posts=all_posts)


@app.route("/post/", methods=["GET", "POST"])
def entry():
    form = EntryForm()
    errors = None
    if request.args.get("new"):
        if form.validate_on_submit():
            is_published = form.is_published.data
            if is_published == True:
                entry = Entry(title=form.title.data, body=form.body.data, is_published=form.is_published.data)
                db.session.add(entry)
                db.session.commit()
                flash("Your Post has been published!", "info")
                return redirect("/")
            else:
                entry = Entry(title=form.title.data, body=form.body.data, is_published=form.is_published.data)
                db.session.add(entry)
                db.session.commit()
                flash("Post created but not published!", "info")
                return redirect("/")
        else:
            errors = form.errors
    elif request.args.get("edit"):

        entry = Entry.query.filter_by(id=entry_id).first_or_404()
        form = EntryForm(obj=entry)
        errors = None
        if form.validate_on_submit():
            form.populate_obj(entry)
            db.session.commit()
            flash("Your Post has been updated!", "info")
            return redirect("/")
        else:
            errors = form.errors

    return render_template("entry_form.html", form=form, errors=errors)


@app.route("/contact/", methods=["GET", "POST"])
def contact():
    return render_template("contact.html")