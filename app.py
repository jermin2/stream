from flask import Flask, render_template, request

app = Flask(__name__)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/register", methods=["POST", "GET"])
def register():

    if request.method == "GET":
        return render_template("register.html")

    if request.method == "POST":
        return "registered succesfully"
