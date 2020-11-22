import requests

from functools import wraps
from flask import g, request, redirect, url_for, session, flash, render_template, make_response
from werkzeug.security import generate_password_hash
from datetime import datetime


def register_user(db, username, password, email, created_on):
    db.execute("INSERT INTO users(username, password, email, created_on) VALUES(:username, :password, :email, :created_on)",
               {"username": username, "password": generate_password_hash(password, method='pbkdf2:sha256', salt_length=8), "email": email, "created_on": created_on})
    db.commit()


def username_exist(db, username):
    return db.execute("SELECT EXISTS(SELECT 1 FROM users WHERE username = :username)", {"username": username}).fetchone()[0]


def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if session.get("user_id") is None:
            flash("Login required!", 'danger')
            return redirect(url_for('login', next=request.url))
        return f(*args, **kwargs)
    return decorated_function


def logout_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if session.get("user_id") is not None:
            flash("Access denied!", 'danger')
            return make_response(render_template("apology.html", apology="403 Forbidden", logout="true"), 403)
        return f(*args, **kwargs)
    return decorated_function


def curr_time():
    return datetime.now().strftime('%Y-%m-%d %H:%M:%S')


def can_post(db, user_id, book_id):
    if db.execute("SELECT review_id FROM reviews WHERE user_id = :user_id AND book_id = :book_id", {"user_id": user_id, "book_id": book_id}).fetchone():
        return False
    return True


def goodreads_info(isbn):
    try:
        res = requests.get("https://www.goodreads.com/book/review_counts.json",
                           params={"key": "rqI7ygPn1I9O8hWG4Y18Q", "isbns": isbn}).json()["books"][0]
        return res
    except BaseException:
        return False
