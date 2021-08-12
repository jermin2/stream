from flask import Flask, flash, redirect, render_template, request, session, current_app, g
from flask_session import Session

from datetime import date

import sqlite3
from sqlite3 import Error

from passlib.hash import sha256_crypt

app = Flask(__name__)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
app.config['DATABASE'] = "stream.db"
Session(app)

countries = ["NZ", "Australia", "Fiji", "Samoa", "Solomon Islands"]

def create_connection(path):
    connection = None
    try:
        connection = sqlite3.connect(path)
        print("Connection to SQLite DB successful")
    except Error as e:
        print(f"The error '{e}' occurred")

    return connection

db = create_connection("stream.db")

# https://flask.palletsprojects.com/en/2.0.x/tutorial/database/
def get_db():
    if 'db' not in g:
        g.db = sqlite3.connect(
            current_app.config['DATABASE'],
            detect_types=sqlite3.PARSE_DECLTYPES
        )
        g.db.row_factory =  sqlite3.Row
    
    return g.db

def close_db(e=None):
    db = g.pop('db', None)

    if db is not None:
        db.close()


@app.route("/")
def index():

    return render_template("index.html")

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":

        email = request.form.get("email").lower()
        password = request.form.get("password")
        db = get_db()
        error = None
        user = db.execute(
            'SELECT * FROM users WHERE email = ?', (email, )
        ).fetchone()

        # Check is user is found
        if user is None:
            error = "Invalid Email"
        # Check password is correct
        elif not sha256_crypt.verify(password, str(user['hash']) ):
            error = "Incorrect password."

        if error is None:
            session.clear()
            session["name"] = email
            flash("Logged in")

            return redirect("/update")

        flash(error)

        
    return render_template("login.html")

@app.route("/logout")
def logout():
    session["name"] = None
    flash("Logged out")
    return redirect("/")
    
@app.route("/register", methods=["POST", "GET"])
def register():

    if session.get("name"):
        return redirect("/logout")

    # If user has already logged in, send them to the update page
    if session.get("name"):
        return redirect("/update")

    # Show the registration form
    if request.method == "GET":
        return render_template("register.html")

    # Register a new user
    if request.method == "POST":
        email = request.form.get("email")
        password = request.form.get("password")
        db = get_db()
        error = None

        # Length of password 8 or greater
        if len(password) < 8:
            error = "Password must be 8 characters long"
        # Confirmation password must match
        elif password != request.form.get("confirm_password"):
            error = "Passwords do not match"
        # Check if user already exists
        elif db.execute(
            'SELECT id FROM users WHERE email = ?', (email, )
        ).fetchone() is not None:
            error = f"User {email} is already registered."

        if error is None:
            db.execute(
                'INSERT INTO users (email, hash) VALUES (?, ?)',
                (email, sha256_crypt.encrypt(password))
            )
            db.commit()

            session["name"] = email
            flash("Logged in")

            return redirect('/update')
        
        # TODO
        flash(error)
        return redirect('/register')
        
@app.route("/update", methods=["POST", "GET"])
def update():

    if not session.get("name"):
        return redirect("/login")

    # Fetch the users details to display
    if request.method == "GET":
        ### TODO ###
        email = session.get("name")
        db = get_db()

        user_id = db.execute( 
            ' SELECT id FROM users WHERE email = ?', (email,)
        ).fetchone()['id']

        if user_id is not None:
            user = db.execute( 
                ' SELECT * FROM addresses WHERE user_id = ? ', (user_id,)
            ).fetchone()
        
        return render_template("update.html", countries=countries, user=user, email=email)

    # Update the users details
    if request.method == "POST":

        # Check if details exist
        fName = request.form.get("first_name")
        lName = request.form.get("last_name")
        address = request.form.get("address")
        village = request.form.get("village")
        suburb = request.form.get("suburb")
        city = request.form.get("city")
        zip_code = request.form.get("zip")
        country = request.form.get("country")
        province = request.form.get("province")
        inactive = "1" if request.form.get("active") != "1" else None
        phone = request.form.get("phone")
        
        today = date.today().strftime("%d/%m/%Y")

        email = session.get("name")
        db = get_db()

        # Find the user id
        user_id = db.execute( 
            ' SELECT id FROM users WHERE email = ?', (email,)
        ).fetchone()['id']

        # Check if data already exists
        if db.execute(
            ' SELECT * FROM addresses WHERE user_id = ?', (user_id, )
        ).fetchone() is None:
            # if user does not exist, add the new info to the database
            db.execute(
                ' INSERT INTO addresses (first_name, last_name, user_id, address, village, suburb, zip, province, city, country, inactive, phone, date_start) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)',
                (fName, lName, user_id, address, village, suburb, zip_code, province, city, country, inactive, phone, today)
            )
            db.commit()





        else:
            #if user exist, update the database
            db.execute(
                'UPDATE addresses SET first_name = ?, last_name = ?, address = ?, village = ?, suburb = ?, zip = ?, province = ?, city = ?, country = ?, inactive = ?, phone = ? WHERE user_id = ?',
                (fName, lName, address, village, suburb, zip_code, province, city, country, inactive, phone, user_id)
            )
            db.commit()
            flash("Details updated")

        return redirect('/update')

        
@app.route("/about", methods=["GET"])
def about():
    return render_template("about.html")