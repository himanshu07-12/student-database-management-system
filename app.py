from flask import Flask, render_template, request, redirect
from auth import login
from students import view_students,insert_student, update_student, delete_student

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

    students = view_students()
    print(students)

    return render_template(
        "students.html",
        students=students
    )


@app.route("/add", methods=["GET", "POST"])
def add_page():

    if request.method == "POST":

        adm = request.form["admno"]
        fname = request.form["fname"]
        lname = request.form["lname"]
        roll = request.form["roll"]
        mobno = request.form["mobno"]

        success, message = insert_student(
            adm,
            fname,
            lname,
            roll,
            mobno
        )

        if success:
            return redirect("/students")

        return message

    return render_template("add_student.html")


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