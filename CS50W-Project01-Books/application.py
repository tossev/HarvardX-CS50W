import os
import requests

from flask import Flask, session, request, render_template, flash, session, url_for, redirect, jsonify
from flask_session import Session
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from helpers import login_required, username_exist, register_user, logout_required, curr_time, can_post, goodreads_info
from werkzeug.security import check_password_hash
from forms import LoginForm, RegistrationForm, SearchForm, Comment
from flask_paginate import Pagination, get_page_parameter, get_page_args

app = Flask(__name__)

# Please note that these credentials are not permanent.

# Heroku rotates credentials periodically and updates applications where this database is attached.

# Host
# ec2-46-137-188-105.eu-west-1.compute.amazonaws.com

# Database
# d9nf8gmbg9nim4

# User
# naderpeswwpwxm

# Port
# 5432

# Password
# e47683652f35dcaef4a25bfa022e695df0ea3797fc6d84969413ce29f2bdf556

# URI
# postgres://naderpeswwpwxm:e47683652f35dcaef4a25bfa022e695df0ea3797fc6d84969413ce29f2bdf556@ec2-46-137-188-105.eu-west-1.compute.amazonaws.com:5432/d9nf8gmbg9nim4

# Heroku CLI
# heroku pg:psql postgresql-acute-42153 --app book-review-tsv

# Check for environment variable
if not os.getenv("DATABASE_URL"):
    raise RuntimeError("DATABASE_URL is not set")

app.config["SECRET_KEY"] = "f4328f2e66751f1b4fd822221c0f30d2"

# Configure session to use filesystem
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"

# Ensure templates are auto-reloaded
app.config["TEMPLATES_AUTO_RELOAD"] = True
Session(app)

# Set up database
engine = create_engine(os.getenv("DATABASE_URL"))
db = scoped_session(sessionmaker(bind=engine))


@app.route("/register", methods=['GET', 'POST'])
@logout_required
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        if username_exist(db, form.username.data):
            return render_template("register.html", title="Register", form=form, username_exist="Username already exists.")

        register_user(db, form.username.data, form.password.data,
                      form.email.data, curr_time())

        flash(f'An account created for {form.username.data}', 'success')
        return redirect(url_for("login"))

    return render_template("register.html", title="Register", form=form)


@app.route("/", methods=['GET'])
@logout_required
def index():
    return redirect(url_for("login"))


@app.route("/login", methods=['GET', 'POST'])
@logout_required
def login():
    form = LoginForm()
    if form.validate_on_submit():
        if not username_exist(db, form.username.data):
            return render_template("login.html", title="Login", form=form, username_doesnt_exist="Username doesn't exists.")

        password_hash = db.execute("SELECT password FROM users WHERE username=:username", {
                                   "username": form.username.data}).fetchone()[0]

        if check_password_hash(password_hash, form.password.data):
            # Update 'last_login' field
            session["last_login"] = db.execute("SELECT last_login FROM users WHERE username = :username", {
                                               "username": form.username.data}).fetchone()[0]
            db.execute("UPDATE users SET last_login= :last_login WHERE username = :username", {
                       "last_login": curr_time(), "username": form.username.data})
            db.commit()

            session["user_id"] = db.execute("SELECT user_id FROM users WHERE username = :username", {
                                            "username": form.username.data}).fetchone()[0]
            session["username"] = form.username.data
            session["email"] = db.execute("SELECT email FROM users WHERE username = :username", {
                                          "username": form.username.data}).fetchone()[0]
            session["registration_date"] = db.execute("SELECT created_on FROM users WHERE username = :username", {
                                                      "username": form.username.data}).fetchone()[0]

            flash("Login successful", "success")
            return redirect(url_for("search"))
        else:
            return render_template("login.html", title="Login", form=form, incorrect_password="Incorrect password.")

    return render_template('login.html', title='Login', form=form)


@app.route("/logout", methods=['GET', 'POST'])
@login_required
def logout():
    session.clear()
    flash("Logged out.", 'success')
    return redirect(url_for("login"))


@app.route("/search", methods=['GET', 'POST'])
@login_required
def search():
    form = SearchForm()

    if form.validate_on_submit():
        column = form.select.data
        query = form.search.data

        return redirect(url_for('search_result', column=column, query=query))

    return render_template("search.html", title="Search", form=form)


@app.route("/search/result/<string:column>/<string:query>", methods=['GET', 'POST'])
@login_required
def search_result(column, query):
    if request.method == 'GET':
        result = db.execute(
            f"SELECT * FROM books WHERE {column} LIKE '%{query}%'").fetchall()
        page, per_page, offset = get_page_args(page_parameter='page',
                                               per_page_parameter='per_page')
        pagination_records = result[offset: offset + per_page]
        pagination = Pagination(record_name="books",
                                show_single_page=False,
                                page=page,
                                per_page=per_page,
                                total=len(result),
                                css_framework='bootstrap4')

        return render_template("search-results.html",
                               pagination=pagination,
                               title="Search results",
                               records=pagination_records,
                               column=column,
                               query=query,
                               page=page,
                               per_page=per_page,
                               result=result)


@app.route("/book/<string:title>", methods=['GET', 'POST'])
@login_required
def book(title):
    form = Comment()
    book = db.execute(
        f"SELECT * FROM books WHERE title = '{title}'").fetchone()
    # prevent searching in browser url field
    try:
        reviews = db.execute(
            "SELECT * FROM reviews WHERE book_id = :book_id", {"book_id": book[0]}).fetchall()
    except BaseException:
        return redirect(url_for('search'))

    if form.validate_on_submit():
        flash("Review submited", 'success')
        comment = form.comment.data
        rating = form.rate.data
        db.execute("""INSERT INTO reviews(user_id, book_id, rating, comment, created_on) 
                   VALUES(:user_id, :book_id, :rating, :comment, :created_on)""",
                   {"user_id": session["user_id"], "book_id": book[0], "rating": rating, "comment": comment, "created_on": curr_time()})
        db.commit()

        return redirect(url_for('book', title=title))

    return render_template("book.html",
                           title=book[2],
                           book=book,
                           form=form,
                           can_post=can_post(db, session["user_id"], book[0]),
                           reviews=reviews,
                           goodreads=goodreads_info(book[1]))


@app.route("/api/<string:isbn>", methods=['GET'])
def api(isbn):
    book_info = db.execute("SELECT * FROM books WHERE isbn = :isbn", {
        "isbn": isbn}).fetchone()
    if book_info is None:
        return jsonify({"error": "Invalid isbn"}), 404

    book_id = book_info[0]
    title = book_info[2]
    author = book_info[3]
    year = book_info[4]
    review_count = db.execute("SELECT COUNT(comment) FROM reviews WHERE book_id = :book_id", {
                              "book_id": book_id}).fetchone()[0]
    average_score = db.execute("SELECT AVG(rating) FROM reviews WHERE book_id = :book_id", {
                               "book_id": book_id}).fetchone()[0]
    if not average_score:
        average_score = 0

    return jsonify({
        "title": title,
        "author": author,
        "year": year,
        "isbn": isbn,
        "review_count": review_count,
        "average_score": round(float(average_score), 2)
    })
