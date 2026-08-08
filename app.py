from flask import Flask, render_template, request, redirect, session, flash
from auth import login
import csv
import sqlite3
from io import StringIO
from flask import make_response
from utils import login_required
from students import view_students,insert_student, update_student, delete_student, search_student, get_student, get_dashboard_stats
from students import  get_recent_students
app = Flask(__name__)
app.secret_key = "student_database_secret_key"

@app.route("/")
def home():

    student_count, user_count = get_dashboard_stats()

    return render_template(
        "index.html",
        total_students=student_count,
        total_admins=user_count
    )

@app.route("/login", methods=["GET", "POST"])
def login_page():

    if request.method == "POST":

        login_id = request.form["login_id"]
        username = request.form["username"]
        password = request.form["password"]

        success = login(login_id, username, password)

        if success:
           session["user"] = username
           flash("Login Successful!", "success")
           return redirect("/dashboard")

        else:
            flash("Invalid Login ID, Username or Password!", "danger")
            return redirect("/login")

    return render_template("login.html")
    

@app.route("/dashboard")
@login_required
def dashboard():
    student_count, user_count = get_dashboard_stats()
    recent_students = get_recent_students()
    return render_template(
    "dashboard.html",
    student_count=student_count,
    user_count=user_count,
    recent_students=recent_students
)

@app.route("/students")
@login_required
def students_page():

    keyword = request.args.get("keyword", "").strip()

    if keyword:
        students = search_student(keyword)
    else:
        students = view_students()

    return render_template(
        "students.html",
        students=students,
        keyword=keyword
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
            flash(message, "success")
            return redirect("/students")
        else:
            flash(message, "danger")
            return redirect("/add")

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
            flash(message, "success")
            return redirect("/students")
        else:
            flash(message, "danger")
            return redirect(f"/update/{adm}")

    student=get_student(adm)

    return render_template(
        "update_student.html",
        student=student
    )


@app.route("/delete/<int:adm>")
@login_required
def delete_page(adm):

    success, message = delete_student(adm)

    if success:
        flash(message, "success")
    else:
        flash(message, "danger")

    return redirect("/students")


@app.route("/logout")
def logout():
    session.clear()
    return redirect("/")


@app.route("/export")
@login_required
def export_students():

    students = view_students()

    output = StringIO()

    writer = csv.writer(output)

    writer.writerow([
        "Admission No",
        "First Name",
        "Last Name",
        "Roll No",
        "Mobile"
    ])

    for student in students:

        writer.writerow([
            student["admno"],
            student["fname"],
            student["lname"],
            student["roll"],
            student["mobno"]
        ])

    response = make_response(output.getvalue())

    response.headers["Content-Disposition"] = \
        "attachment; filename=students.csv"

    response.headers["Content-type"] = "text/csv"

    return response

@app.after_request
def add_header(response):

    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Pragma"] = "no-cache"
    response.headers["Expires"] = "0"

    return response

if __name__ == "__main__":
    app.run(debug=True)