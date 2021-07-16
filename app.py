from flask import Flask, redirect, render_template, request, session
from flask_session import Session

import sqlite3
from sqlite3 import Error

from passlib.hash import sha256_crypt

app = Flask(__name__)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

countries = ["NZ", "AUS", "Fiji", "Samoa"]

def create_connection(path):
    connection = None
    try:
        connection = sqlite3.connect(path)
        print("Connection to SQLite DB successful")
    except Error as e:
        print(f"The error '{e}' occurred")

    return connection

def execute_query(connection, query, variables):
    cursor = connection.cursor()
    try:
        cursor.execute(query, variables)
        connection.commit()
        print("Query executed succesfully")
        return 

    except Error as e:
        print(f"the error '{e}' occurred")

def select_person(connection, name):
    """
    Query all the rows in the user table for the given user email
    :param connection: the Connection object
    :return:
    """
    cur = connection.cursor()
    try:
        cur.execute("""SELECT * FROM users WHERE email = ?""", name)
        print("Query executed succesfully")
        return cur.fetchone()
    
    except Error as e:
        print(f"the error '{e}' occurred")



@app.route("/")
def index():
    if not session.get("name"):
        return redirect("/login")
    return render_template("index.html")

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":

        db = create_connection("stream.db")
        with db:
            result = select_person(db, (request.form.get("email").lower(),))
        
        if not result or len(result) < 1:
            return render_template("login.html")

        verified = sha256_crypt.verify(request.form.get("password"), str(result[5]))

        if verified:
            session["name"] = request.form.get("name")
            return redirect("/update")
        
    return render_template("login.html")

@app.route("/logout")
def logout():
    session["name"] = None
    return redirect("/")
    
@app.route("/register", methods=["POST", "GET"])
def register():

    # Show the registration form
    if request.method == "GET":
        return render_template("register.html")

    # Register a new user
    if request.method == "POST":
        if len(request.form.get("password")) < 8:
            return "password must be 8 characters long"
        if request.form.get("password") != request.form.get("confirm_password"):
            return "passwords do not match"

        db = create_connection("stream.db")
        with db:
            result = select_person(db, (request.form.get("email").lower(),))

        # If user already exists, return a emssage
        if result and len(result) > 0:
            return "user already exists"
        else:
            hash = sha256_crypt.encrypt(request.form.get("password"))
            execute_query(db, "INSERT INTO users(email, hash) VALUES(?,?)", (request.form.get("email"), hash) )
            return "registered succesfully"

@app.route("/update", methods=["POST", "GET"])
def update():

    # Fetch the users details to display
    if request.method == "GET":
        return render_template("update.html", countries=countries)

    # Update the users details
    if request.method == "POST":
        return "NOT YET IMPLEMENTED"