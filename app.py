from flask import Flask, render_template, request, redirect
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
            return redirect("/dashboard")

        else:
            return "Invalid Credentials"

    return render_template("login.html")


@app.route("/signup")
def signup():
    return render_template("signup.html")

@app.route("/dashboard")
def dashboard():
    return render_template("dashboard.html")

@app.route("/students")
def students_page():
    return "Students Page"


@app.route("/add")
def add_page():
    return "Add Student Page"


@app.route("/update")
def update_page():
    return "Update Student Page"


@app.route("/delete")
def delete_page():
    return "Delete Student Page"


@app.route("/logout")
def logout():
    return redirect("/")

@app.route("/search")
def search_page():
    return "Search Student Page"


if __name__ == "__main__":
    app.run(debug=True)