import os

from flask import Flask, session, render_template, request, flash, redirect, url_for, abort, jsonify
from flask_session import Session
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
import requests

app = Flask(__name__)

# Check for environment variable
if not os.getenv("DATABASE_URL"):
    raise RuntimeError("DATABASE_URL is not set")

# Configure session to use filesystem
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Set up database
engine = create_engine(os.getenv("DATABASE_URL"))
db = scoped_session(sessionmaker(bind=engine))


@app.before_request
def ensure_session_username():
    if not session.get("username"): session["username"] = ''

@app.route("/")
def index():
    return render_template("home.html")

@app.route("/signup", methods=["GET", "POST"])
def signup():
    if request.method == "GET":
        return render_template("signup.html")

    username = request.form.get("username")
    password = request.form.get("password")

    if not username or not password:
        flash("Username and password cannot be blank")
        return render_template("signup.html")
    if db.execute("SELECT * FROM users WHERE username = :username", {"username": username}).rowcount > 0:
        flash("Username has already been taken")
        return render_template("signup.html")

    db.execute("INSERT INTO users (username, password) VALUES (:username, :password)", {"username": username, "password": password})
    db.commit()
    user = db.execute("SELECT * FROM users WHERE username = :username", {"username": username}).fetchone()
    session["username"] = user.username

    return render_template("search.html")

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "GET":
        return render_template("login.html")

    username = request.form.get("username")
    password = request.form.get("password")

    if not username or not password:
        flash("Username and password cannot be blank")
        return render_template("login.html")

    user = db.execute("SELECT * FROM users WHERE username = :username AND password = :password", {"username": username, "password": password}).fetchone()
    if not user:
        flash("Username or password is incorrect")
        return render_template("login.html")

    session["username"] = user.username

    return render_template("search.html")

@app.route("/logout")
def logout():
    session["username"] = ''
    return render_template("home.html")

@app.route("/search")
def search():
    if not session["username"]:
        redirect(url_for('login'))

    query = request.args.get("query")
    results = []

    if query:
        results = db.execute("SELECT books.id AS id, books.isbn AS isbn, books.title AS title, authors.name AS author_name FROM books INNER JOIN authors ON books.author_id = authors.id WHERE books.isbn ILIKE :query OR books.title ILIKE :query OR authors.name ILIKE :query",
                                {"query": f"%{query}%"}).fetchall()

    return render_template("search.html", query=query, results=results)

@app.route("/books/<int:id>")
def show_book(id):
    if not session["username"]:
        redirect(url_for('login'))

    book = db.execute("SELECT books.id AS id, books.isbn AS isbn, books.title AS title, authors.name AS author_name FROM books INNER JOIN authors ON books.author_id = authors.id WHERE books.id = :id",
                        {"id": id}).fetchone()

    if not book:
        abort(404)

    response = requests.get("https://goodreads.com/book/review_counts.json",
                            params={"key": "dYolMNb3RBl70KPWjAKMA", "isbns": book.isbn})
    goodreads_book = response.json()["books"][0]
    goodreads_avg_rating = goodreads_book["average_rating"]
    goodreads_ratings_count = goodreads_book["ratings_count"]

    reviews = db.execute("SELECT ubr.opinion AS opinion, ubr.rating AS rating, users.username AS username FROM user_book_reviews ubr INNER JOIN users ON ubr.user_id = users.id WHERE ubr.book_id = :id",
                            {"id": id}).fetchall()
    can_write_review = session["username"] not in list(map(lambda review: review.username, reviews))

    return render_template("book.html", book=book,
                            goodreads_avg_rating=goodreads_avg_rating,
                            goodreads_ratings_count=goodreads_ratings_count,
                            reviews=reviews, can_write_review=can_write_review)

@app.route("/books/<int:id>/reviews", methods=["POST"])
def add_review(id):
    if not session["username"]:
        redirect(url_for('login'))

    book = db.execute("SELECT * FROM books WHERE id = :id",
                        {"id": id}).fetchone()
    if not book:
        render_template("error.html", message="Book does not exist.")

    user = db.execute("SELECT * FROM users WHERE username = :username",
                        {"username": session["username"]}).fetchone()
    if not user:
        render_template("error.html", message="User does not exist.")

    existing_review = db.execute("SELECT * FROM user_book_reviews WHERE book_id = :book_id AND user_id = :user_id",
                                {"book_id": book.id, "user_id": user.id}).fetchone()
    if existing_review:
        render_template("error.html", message="You had already written a review for this book.")

    rating = request.form.get("rating")
    opinion = request.form.get("opinion")

    db.execute("INSERT INTO user_book_reviews (rating, opinion, book_id, user_id) VALUES (:rating, :opinion, :book_id, :user_id)",
                {"rating": rating, "opinion": opinion, "book_id": book.id, "user_id": user.id})
    db.commit()

    return redirect(url_for("show_book", id=book.id))

@app.route("/api/<string:isbn>")
def api(isbn):
    book = db.execute("SELECT books.title AS title, books.isbn AS isbn, books.year AS year, authors.name AS author_name FROM books INNER JOIN authors ON books.author_id = authors.id WHERE books.isbn = :isbn",
                        {"isbn": isbn}).fetchone()
    if not book:
        abort(404)

    response = requests.get("https://goodreads.com/book/review_counts.json",
                            params={"key": "dYolMNb3RBl70KPWjAKMA", "isbns": isbn})
    goodreads_book = response.json()["books"][0]

    return jsonify({
        "title": book.title,
        "author": book.author_name,
        "year": book.year,
        "isbn": book.isbn,
        "review_count": goodreads_book["ratings_count"],
        "average_score": float(goodreads_book["average_rating"]),
    })
