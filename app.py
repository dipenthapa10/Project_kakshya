from flask import Flask, request, render_template, redirect, url_for
from config import get_connection
from models import *

app = Flask(__name__)

@app.route("/")
def index():
    return render_template("index.html")

###### ADMIN ######

@app.route("/admin/dashboard")
def admin_dashboard():
    return render_template("dashboard.html")


@app.route("/admin/courses/courses")
def admin_courses():
    data = get_courses()
    return render_template("admin/courses/courses.html", courses = data)

@app.route("/admin/courses/add", methods=["GET", "POST"])
def add_course():
    if request.method == "POST":
        name = request.form["name"]
        course_no = request.form["course_no"]
        title = request.form["title"]
        credits = request.form["credits"]

        insert_course(name, course_no, title, credits)
        return redirect("/admin/courses")
    
    # get all departments for dropdown
    departments = get_departments()
    return render_template("admin/courses/add.html", departments=departments)


@app.route("/admin/courses/edit/<int:course_id>", methods=["GET", "POST"])
def edit_course(course_id):
    course = get_course_by_id(course_id)

    if request.method == "POST":
        dept_ID = request.form["dept_ID"]
        course_no = request.form["course_no"]
        title = request.form["title"]
        credits = request.form["credits"]

        update_course(course_id, dept_ID, course_no, title, credits)
        return redirect("/admin/courses")

    return render_template("admin/courses/edit.html", course=course)


@app.route("/admin/courses/delete/<int:course_id>")
def delete_course_route(course_id):
    delete_course(course_id)
    return redirect("/admin/courses")


@app.route("/admin/departments")
def admin_departments():
    return render_template("admin/departments.html")

@app.route("/admin/students")
def admin_students():
    return render_template("admin/students.html")


@app.route("/admin/instructors")
def admin_instructors():
    return render_template("admin/instructors.html")


####### INSTRUCTOR #######
@app.route("/instructor")
def instructor_dashboard():
    return render_template("instructor/dashboard.html")


####### STUDENT #######
@app.route("/student")
def student_dashboard():
    return render_template("student/dashboard.html")








if __name__ == "__main__":
    app.run(debug = True)



