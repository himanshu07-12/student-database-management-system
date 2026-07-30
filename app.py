from flask import Flask, render_template, request, redirect, session
from auth import login
from utils import login_required
from students import view_students,insert_student, update_student, delete_student, search_student, get_student

app = Flask(__name__)
app.secret_key = "student_database_secret_key"

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
           session["user"] = username
           return redirect("/dashboard")

        else:
            return "Invalid Credentials"

    return render_template("login.html")


@app.route("/signup")
def signup():
    return render_template("signup.html")

@app.route("/dashboard")
@login_required
def dashboard():
    return render_template("dashboard.html")

@app.route("/students")
@login_required
def students_page():

    students = view_students()
    print(students)

    return render_template(
        "students.html",
        students=students
    )


@app.route("/add", methods=["GET", "POST"])
@login_required
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


@app.route("/update/<int:adm>", methods=["GET","POST"])
@login_required
def update_page(adm):

    if request.method=="POST":

        fname=request.form["fname"]
        lname=request.form["lname"]
        roll=request.form["roll"]
        mobno=request.form["mobno"]

        success,message=update_student(
            adm,
            fname,
            lname,
            roll,
            mobno
        )

        if success:
            return redirect("/students")

        return message

    student=get_student(adm)

    return render_template(
        "update_student.html",
        student=student
    )


@app.route("/delete/<int:adm>")
@login_required
def delete_page(adm):

    success, message = delete_student(adm)

    return redirect("/students")


@app.route("/logout")
def logout():
    session.clear()
    return redirect("/")

@app.route("/search", methods=["GET", "POST"])
@login_required
def search_page():

    students = []

    if request.method == "POST":

        keyword = request.form["keyword"]

        students = search_student(keyword)

    return render_template(
        "search.html",
        students=students
    )

if __name__ == "__main__":
    app.run(debug=True)