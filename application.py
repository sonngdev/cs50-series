import os

from flask import Flask, session, render_template, request, flash, redirect, url_for
from flask_session import Session
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker

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
def ensure_session_user_id():
    if not session.get("user_id"): session["user_id"] = 0

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
    session["user_id"] = user.id

    return render_template("home.html")

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

    session["user_id"] = user.id

    return render_template("home.html")

@app.route("/logout")
def logout():
    session["user_id"] = 0
    return render_template("home.html")
