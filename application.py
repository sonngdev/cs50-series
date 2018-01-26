from cs50 import SQL
from flask import Flask, flash, redirect, render_template, request, session
from flask_session import Session
from tempfile import mkdtemp
from werkzeug.exceptions import default_exceptions
from werkzeug.security import check_password_hash, generate_password_hash
from datetime import datetime

from helpers import apology, login_required, lookup, usd

# Configure application
app = Flask(__name__)


# Ensure responses aren't cached
@app.after_request
def after_request(response):
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response


# Custom filter
app.jinja_env.filters["usd"] = usd

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_FILE_DIR"] = mkdtemp()
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Configure CS50 Library to use SQLite database
db = SQL("sqlite:///finance.db")


@app.route("/")
@login_required
def index():
    """Show portfolio of stocks"""
    # Query database for user history and cash
    rows = db.execute("SELECT * FROM stocks WHERE id = :i", i=session["user_id"])
    cash = db.execute("SELECT cash FROM users WHERE id = :i", i=session["user_id"])

    # Stocks shares, current price, and total value
    stocks = {}
    total = float(cash[0]["cash"])
    for row in rows:
        stocks[row["symbol"]] = {"shares": row["shares"], "price": 0, "total": 0}
    for stock in stocks:
        stocks[stock]["price"] = lookup(stock)["price"]
        stocks[stock]["total"] = stocks[stock]["shares"] * stocks[stock]["price"]
        total += stocks[stock]["total"]
        stocks[stock]["price"] = usd(stocks[stock]["price"])
        stocks[stock]["total"] = usd(stocks[stock]["total"])

    return render_template("index.html", keys=sorted(stocks.keys()), stocks=stocks,
                           cash=usd(float(cash[0]["cash"])), total=usd(total))


@app.route("/buy", methods=["GET", "POST"])
@login_required
def buy():
    """Buy shares of stock"""
    # User submit form in buy.html
    if request.method == "POST":

        # Ensure symbol was submitted
        if not request.form.get("symbol"):
            return apology("missing symbol", 400)

        # Ensure shares was submitted
        elif not request.form.get("shares"):
            return apology("missing shares", 400)

        elif not request.form.get("shares").isdigit():
            return apology("invalid shares", 400)

        # Look up the stock symbol
        quote = lookup(request.form.get("symbol"))

        # Ensure valid stock symbol
        if not quote:
            return apology("invalid symbol", 400)

        # Query database for amount of cash left
        cash = db.execute("SELECT cash FROM users WHERE id = :i", i=session["user_id"])

        # Ensure cash is sufficient
        if float(cash[0]["cash"]) < quote["price"] * int(request.form.get("shares")):
            return apology("cannot afford", 400)

        # Query database to record transaction history
        # https://stackoverflow.com/questions/415511/how-to-get-current-time-in-python
        db.execute("INSERT INTO history (id, time, symbol, shares, price) VALUES(:i, :t, :s, :sh, :p)",
                   i=session["user_id"], t=datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                   s=quote["symbol"], sh=int(request.form.get("shares")), p=quote["price"])

        # Query database to update user's remaining cash
        db.execute("UPDATE users SET cash = cash - :c WHERE id = :i",
                   c=quote["price"] * int(request.form.get("shares")), i=session["user_id"])

        # Create new stock if it not already existed
        if len(db.execute("SELECT * FROM stocks WHERE id = :i AND symbol = :s",
                          i=session["user_id"], s=quote["symbol"])) == 0:
            db.execute("INSERT INTO stocks (id, symbol, shares) VALUES(:i, :s, 0)",
                       i=session["user_id"], s=quote["symbol"])

        # Query database to update user's stock
        db.execute("UPDATE stocks SET shares = shares + :sh WHERE id = :i AND symbol = :s",
                   sh=int(request.form.get("shares")), i=session["user_id"], s=quote["symbol"])

        # Redirect user to home page
        return redirect("/")

    # User visit buy.html
    else:
        return render_template("buy.html")


@app.route("/history")
@login_required
def history():
    """Show history of transactions"""
    # Query database for transaction history
    entries = db.execute("SELECT * FROM history WHERE id = :i", i=session["user_id"])

    return render_template("history.html", entries=entries)


@app.route("/login", methods=["GET", "POST"])
def login():
    """Log user in"""

    # Forget any user_id
    session.clear()

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

        # Ensure username was submitted
        if not request.form.get("username"):
            return apology("must provide username", 403)

        # Ensure password was submitted
        elif not request.form.get("password"):
            return apology("must provide password", 403)

        # Query database for username
        rows = db.execute("SELECT * FROM users WHERE username = :username",
                          username=request.form.get("username"))

        # Ensure username exists and password is correct
        if len(rows) != 1 or not check_password_hash(rows[0]["hash"], request.form.get("password")):
            return apology("invalid username and/or password", 403)

        # Remember which user has logged in
        session["user_id"] = rows[0]["id"]

        # Redirect user to home page
        return redirect("/")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("login.html")


@app.route("/logout")
def logout():
    """Log user out"""

    # Forget any user_id
    session.clear()

    # Redirect user to login form
    return redirect("/")


@app.route("/quote", methods=["GET", "POST"])
@login_required
def quote():
    """Get stock quote."""
    # User submit form in quote.html
    if request.method == "POST":

        # Look up the stock symbol
        quote = lookup(request.form.get("symbol"))

        # Ensure valid stock symbol
        if not quote:
            return apology("invalid symbol", 400)

        return render_template("quoted.html", name=quote["name"],
                               symbol=quote["symbol"], price=usd(quote["price"]))

    # User visit quote.html
    else:
        return render_template("quote.html")


@app.route("/register", methods=["GET", "POST"])
def register():
    """Register user"""
    # User submit form in register.html
    if request.method == "POST":

        # Ensure username was submitted
        if not request.form.get("username"):
            return apology("missing username", 400)

        # Ensure password was submitted
        elif not request.form.get("password"):
            return apology("missing password", 400)

        # Ensure password confirmation was submitted
        elif not request.form.get("confirmation"):
            return apology("missing password confirmation", 400)

        # Ensure password and confirmation match
        elif request.form.get("confirmation") != request.form.get("password"):
            return apology("passwords did not match!", 400)

        # Query database to add new user
        result = db.execute("INSERT INTO users (username, hash) VALUES(:u, :h)",
                            u=request.form.get("username"),
                            h=generate_password_hash(request.form.get("password"),
                                                     method="pbkdf2:sha256", salt_length=8))

        # Ensure username is unique
        if not result:
            return apology("username already existed", 400)

        # Remember which user has logged in
        session["user_id"] = result

        # Redirect user to home page
        return redirect("/")

    # User visit register.html
    else:
        return render_template("register.html")


@app.route("/sell", methods=["GET", "POST"])
@login_required
def sell():
    """Sell shares of stock"""
    # Query database for stocks
    rows = db.execute("SELECT * FROM stocks WHERE id = :i", i=session["user_id"])

    # List of stocks names
    symbols = []
    for row in rows:
        symbols.append(row["symbol"].upper())

    # User submit form in sell.html
    if request.method == "POST":

        # Ensure symbol is selected
        if not request.form.get("symbol"):
            return apology("select a symbol", 400)

        # Ensure shares is selected
        if not request.form.get("shares"):
            return apology("missing shares", 400)

        # Ensure positive integer
        if int(request.form.get("shares")) <= 0:
            return apology("invalid shares", 400)

        # Query database for user's stock
        stk = db.execute("SELECT * FROM stocks WHERE id = :i AND symbol = :s",
                         i=session["user_id"], s=request.form.get("symbol").upper())

        # Ensure sufficient shares to sell
        if int(request.form.get("shares")) > stk[0]["shares"]:
            return apology("insufficient shares", 400)

        # Subtract shares
        elif int(request.form.get("shares")) < stk[0]["shares"]:
            db.execute("UPDATE stocks SET shares = shares - :sh WHERE id = :i AND symbol = :s",
                       sh=int(request.form.get("shares")), i=session["user_id"], s=request.form.get("symbol").upper())

        # Delete a stock when its shares reach 0
        else:
            db.execute("DELETE FROM stocks WHERE id = :i AND symbol = :s",
                       i=session["user_id"], s=request.form.get("symbol").upper())

        # Look up stock price
        quote = lookup(request.form.get("symbol"))

        # Query database to record transaction history
        db.execute("INSERT INTO history (id, time, symbol, shares, price) VALUES(:i, :t, :s, :sh, :p)",
                   i=session["user_id"], t=datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                   s=quote["symbol"], sh=-int(request.form.get("shares")), p=quote["price"])

        # Query database to update user's cash
        db.execute("UPDATE users SET cash = cash + :c WHERE id = :i",
                   c=quote["price"] * int(request.form.get("shares")), i=session["user_id"])

        return redirect("/")

    # User visit sell.html
    else:
        return render_template("sell.html", symbols=symbols)


@app.route("/addcash", methods=["GET", "POST"])
@login_required
def addcash():
    """Add additional cash to user account"""
    # User submit form in addcash.html
    if request.method == "POST":

        # Ensure addcash is filled
        if not request.form.get("addcash"):
            return apology("missing cash", 400)

        # Query database to update user's cash
        db.execute("UPDATE users SET cash = cash + :c WHERE id = :i",
                   c=float(request.form.get("addcash")), i=session["user_id"])

        return redirect("/")

    # User visit addcash.html
    else:
        return render_template("addcash.html")


def errorhandler(e):
    """Handle error"""
    return apology(e.name, e.code)


# listen for errors
for code in default_exceptions:
    app.errorhandler(code)(errorhandler)
