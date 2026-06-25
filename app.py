import os
import random
import sqlite3
from flask import Flask, render_template, request, redirect, url_for, flash, session
from flask_wtf import FlaskForm
from werkzeug.security import generate_password_hash, check_password_hash
from wtforms import StringField, DecimalField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Length, Regexp, NumberRange, Email, EqualTo

base_dir = os.path.abspath(os.path.dirname(__file__))
db_path = os.path.join(base_dir, "database.db")

app = Flask(__name__)
app.config["SECRET_KEY"] = "replace-with-a-secure-random-key"
app.config["WTF_CSRF_ENABLED"] = True

class CreateAccountForm(FlaskForm):
    account_name = StringField(
        "Account Holder Name",
        validators=[DataRequired(), Length(min=2, max=100)],
        render_kw={"placeholder": "Full Name"},
    )
    phone_number = StringField(
        "Phone Number",
        validators=[DataRequired(), Regexp(r"^\d{10}$", message="Enter a valid 10-digit phone number.")],
        render_kw={"placeholder": "1234567890"},
    )
    submit = SubmitField("Create Account")

class AmountForm(FlaskForm):
    account_no = StringField(
        "Account Number",
        validators=[DataRequired(), Length(min=10, max=10, message="Enter a 10-digit account number.")],
        render_kw={"placeholder": "1234567890"},
    )
    amount = DecimalField(
        "Amount",
        validators=[DataRequired(), NumberRange(min=0.01, message="Amount must be at least 0.01.")],
        places=2,
        render_kw={"placeholder": "0.00"},
    )
    submit = SubmitField("Submit")

class LoginForm(FlaskForm):
    email = StringField(
        "Email",
        validators=[DataRequired(), Email(message="Enter a valid email address.")],
        render_kw={"placeholder": "you@example.com"},
    )
    password = PasswordField(
        "Password",
        validators=[DataRequired(), Length(min=6, message="Password must be at least 6 characters.")],
        render_kw={"placeholder": "Enter password"},
    )
    submit = SubmitField("Login")

class SignupForm(FlaskForm):
    email = StringField(
        "Email",
        validators=[DataRequired(), Email(message="Enter a valid email address.")],
        render_kw={"placeholder": "you@example.com"},
    )
    password = PasswordField(
        "Password",
        validators=[DataRequired(), Length(min=6, message="Password must be at least 6 characters.")],
        render_kw={"placeholder": "Enter password"},
    )
    confirm_password = PasswordField(
        "Confirm Password",
        validators=[DataRequired(), EqualTo('password', message='Passwords must match.')],
        render_kw={"placeholder": "Repeat password"},
    )
    submit = SubmitField("Sign Up")


def get_db_connection():
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    with get_db_connection() as conn:
        conn.execute(
            """
            CREATE TABLE IF NOT EXISTS accounts (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                account_no TEXT UNIQUE NOT NULL,
                account_name TEXT NOT NULL,
                phone_number TEXT NOT NULL,
                balance REAL DEFAULT 0,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
            """
        )
        conn.execute(
            """
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                email TEXT UNIQUE NOT NULL,
                password_hash TEXT NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
            """
        )
        conn.execute(
            """
            CREATE TABLE IF NOT EXISTS transactions (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                account_no TEXT NOT NULL,
                transaction_type TEXT NOT NULL,
                amount REAL NOT NULL,
                balance_after REAL NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (account_no) REFERENCES accounts(account_no)
            )
            """
        )
        conn.commit()


def generate_unique_account_no():
    conn = get_db_connection()
    try:
        while True:
            account_no = ''.join(str(random.randint(0, 9)) for _ in range(10))
            existing = conn.execute("SELECT 1 FROM accounts WHERE account_no = ?", (account_no,)).fetchone()
            if not existing:
                return account_no
    finally:
        conn.close()


@app.context_processor
def inject_current_user():
    user_id = session.get("user_id")
    if not user_id:
        return dict(current_user=None)
    conn = get_db_connection()
    user = conn.execute("SELECT id, email FROM users WHERE id = ?", (user_id,)).fetchone()
    conn.close()
    return dict(current_user=user)


@app.route("/")
def index():
    conn = get_db_connection()
    stats = conn.execute(
        "SELECT COUNT(*) AS total_accounts, IFNULL(SUM(balance), 0) AS total_balance FROM accounts"
    ).fetchone()
    latest_account = conn.execute(
        "SELECT account_no, account_name, balance, created_at FROM accounts ORDER BY created_at DESC LIMIT 5"
    ).fetchall()
    conn.close()

    return render_template(
        "index.html",
        total_accounts=stats["total_accounts"],
        total_balance=stats["total_balance"],
        total_deposits=stats["total_balance"],
        latest_account=latest_account,
    )


@app.route("/create-account", methods=["GET", "POST"])
def create_account():
    if not session.get("user_id"):
        flash("Please sign up or log in to create an account.", "warning")
        return redirect(url_for("signup"))

    form = CreateAccountForm()
    account_no = None
    if form.validate_on_submit():
        account_name = form.account_name.data.strip()
        phone_number = form.phone_number.data.strip()
        account_no = generate_unique_account_no()

        try:
            conn = get_db_connection()
            conn.execute(
                "INSERT INTO accounts (account_no, account_name, phone_number, balance) VALUES (?, ?, ?, 0)",
                (account_no, account_name, phone_number),
            )
            conn.commit()
            conn.close()
            flash(f"Account created successfully! Account Number: {account_no}", "success")
            return redirect(url_for("create_account"))
        except sqlite3.IntegrityError:
            flash("Unable to create account. Please try again.", "danger")

    return render_template("create_account.html", form=form, account_no=account_no)


@app.route("/signup", methods=["GET", "POST"])
def signup():
    if session.get("user_id"):
        return redirect(url_for("index"))

    form = SignupForm()
    if form.validate_on_submit():
        email = form.email.data.strip().lower()
        password_hash = generate_password_hash(form.password.data)

        try:
            conn = get_db_connection()
            cursor = conn.execute(
                "INSERT INTO users (email, password_hash) VALUES (?, ?)",
                (email, password_hash),
            )
            conn.commit()
            session["user_id"] = cursor.lastrowid
            conn.close()
            flash("Signup successful. Welcome to Union Bank!", "success")
            return redirect(url_for("index"))
        except sqlite3.IntegrityError:
            flash("This email is already registered. Please log in.", "danger")

    return render_template("signup.html", form=form)


@app.route("/login", methods=["GET", "POST"])
def login():
    if session.get("user_id"):
        return redirect(url_for("index"))

    form = LoginForm()
    if form.validate_on_submit():
        email = form.email.data.strip().lower()
        password = form.password.data
        conn = get_db_connection()
        user = conn.execute("SELECT * FROM users WHERE email = ?", (email,)).fetchone()
        conn.close()

        if user and check_password_hash(user["password_hash"], password):
            session["user_id"] = user["id"]
            flash("Logged in successfully.", "success")
            return redirect(url_for("index"))

        flash("Invalid email or password.", "danger")

    return render_template("login.html", form=form)


@app.route("/logout")
def logout():
    session.pop("user_id", None)
    flash("You have been logged out.", "success")
    return redirect(url_for("login"))


@app.route("/deposit", methods=["GET", "POST"])
def deposit():
    form = AmountForm()
    previous_balance = None
    updated_balance = None
    if form.validate_on_submit():
        account_no = form.account_no.data.strip()
        amount = float(form.amount.data)

        conn = get_db_connection()
        account = conn.execute("SELECT * FROM accounts WHERE account_no = ?", (account_no,)).fetchone()

        if account is None:
            flash("Account not found. Please check the account number.", "danger")
        else:
            previous_balance = float(account["balance"])
            updated_balance = previous_balance + amount
            conn.execute(
                "UPDATE accounts SET balance = ? WHERE account_no = ?",
                (updated_balance, account_no),
            )
            conn.execute(
                "INSERT INTO transactions (account_no, transaction_type, amount, balance_after) VALUES (?, ?, ?, ?)",
                (account_no, "Deposit", amount, updated_balance),
            )
            conn.commit()
            flash(f"Deposit successful. New balance for {account_no}: ${updated_balance:,.2f}", "success")
        conn.close()

    return render_template(
        "deposit.html",
        form=form,
        previous_balance=previous_balance,
        updated_balance=updated_balance,
    )


@app.route("/withdraw", methods=["GET", "POST"])
def withdraw():
    form = AmountForm()
    remaining_balance = None
    if form.validate_on_submit():
        account_no = form.account_no.data.strip()
        amount = float(form.amount.data)

        conn = get_db_connection()
        account = conn.execute("SELECT * FROM accounts WHERE account_no = ?", (account_no,)).fetchone()

        if account is None:
            flash("Account not found. Please check the account number.", "danger")
        else:
            current_balance = float(account["balance"])
            if amount > current_balance:
                flash("Insufficient balance for this withdrawal.", "danger")
                remaining_balance = current_balance
            else:
                remaining_balance = current_balance - amount
                conn.execute(
                    "UPDATE accounts SET balance = ? WHERE account_no = ?",
                    (remaining_balance, account_no),
                )
                conn.execute(
                    "INSERT INTO transactions (account_no, transaction_type, amount, balance_after) VALUES (?, ?, ?, ?)",
                    (account_no, "Withdrawal", amount, remaining_balance),
                )
                conn.commit()
                flash(f"Withdrawal successful. Remaining balance: ${remaining_balance:,.2f}", "success")
        conn.close()

    return render_template("withdraw.html", form=form, remaining_balance=remaining_balance)


@app.route("/accounts")
def accounts():
    search_query = request.args.get("search", "").strip()
    page = request.args.get("page", 1, type=int)
    per_page = 10
    offset = (page - 1) * per_page

    conn = get_db_connection()
    if search_query:
        search_term = f"%{search_query}%"
        count_result = conn.execute(
            "SELECT COUNT(*) AS total FROM accounts WHERE account_no LIKE ? OR account_name LIKE ?",
            (search_term, search_term),
        ).fetchone()
        accounts_data = conn.execute(
            "SELECT * FROM accounts WHERE account_no LIKE ? OR account_name LIKE ? ORDER BY created_at DESC LIMIT ? OFFSET ?",
            (search_term, search_term, per_page, offset),
        ).fetchall()
    else:
        count_result = conn.execute("SELECT COUNT(*) AS total FROM accounts").fetchone()
        accounts_data = conn.execute(
            "SELECT * FROM accounts ORDER BY created_at DESC LIMIT ? OFFSET ?",
            (per_page, offset),
        ).fetchall()

    conn.close()
    total_accounts = count_result["total"]
    total_pages = max((total_accounts + per_page - 1) // per_page, 1)

    return render_template(
        "accounts.html",
        accounts=accounts_data,
        search_query=search_query,
        page=page,
        total_pages=total_pages,
        total_accounts=total_accounts,
    )


@app.route("/account/<account_no>")
def account_detail(account_no):
    conn = get_db_connection()
    account = conn.execute("SELECT * FROM accounts WHERE account_no = ?", (account_no,)).fetchone()
    if account is None:
        conn.close()
        flash("Account not found.", "danger")
        return redirect(url_for("accounts"))

    transactions = conn.execute(
        "SELECT * FROM transactions WHERE account_no = ? ORDER BY created_at DESC",
        (account_no,),
    ).fetchall()
    conn.close()

    return render_template(
        "account_detail.html",
        account=account,
        transactions=transactions,
    )


if __name__ == "__main__":
    init_db()
    app.run(debug=True)
