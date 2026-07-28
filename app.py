from flask import Flask, render_template, request
from auth import login

app = Flask(__name__)

@app.route("/")
def home():
    return render_template("index.html")


@app.route("/login", methods=["GET", "POST"])
def login_page():

    if request.method == "POST":

        login_id = request.form["login_id"]
        username = request.form["username"]
        password = request.form["password"]

        success = login(login_id, username, password)

        if success:
            return "Login Successful"

        else:
            return "Invalid Credentials"

    return render_template("login.html")


@app.route("/signup")
def signup():
    return render_template("signup.html")


if __name__ == "__main__":
    app.run(debug=True)