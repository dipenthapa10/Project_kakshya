from flask import Flask, request, render_template, redirect, url_for
from config import get_connection
from models import *
from helper import *

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
    departments = get_departments()  # must be loaded BEFORE render

    if request.method == "POST":
        dept_ID = request.form["dept_ID"]
        course_no = request.form["course_no"]
        title = request.form["title"]
        credits = request.form["credits"]

        update_course(course_id, dept_ID, course_no, title, credits)
        return redirect("/admin/courses")

    return render_template(
        "admin/courses/edit.html",
        course=course,
        departments=departments
    )


 


@app.route("/admin/courses/delete/<int:course_id>")
def delete_course_route(course_id):
    delete_course(course_id)
    return redirect("/admin/courses")



###########   DEPARTMENTS (ADMIN)


@app.route("/admin/departments")
def admin_departments():
    departments = get_all_departments()
    return render_template("admin/departments/list.html", departments=departments)


@app.route("/admin/departments/add", methods=["GET", "POST"])
def add_department():
    if request.method == "POST":
        name = request.form["name"]
        building = request.form["building"]

        insert_department(name, building)
        return redirect("/admin/departments")

    return render_template("admin/departments/add.html")


@app.route("/admin/departments/edit/<int:dept_id>", methods=["GET", "POST"])
def edit_department(dept_id):
    department = get_department_by_id(dept_id)

    if request.method == "POST":
        name = request.form["name"]
        building = request.form["building"]

        update_department(dept_id, name, building)
        return redirect("/admin/departments")

    return render_template("admin/departments/edit.html", department=department)


@app.route("/admin/departments/delete/<int:dept_id>")
def delete_department_route(dept_id):
    delete_department(dept_id)
    return redirect("/admin/departments")



#   SECTIONS (ADMIN)


@app.route("/admin/sections")
def admin_sections():
    sections = get_all_sections()
    return render_template("admin/sections/list.html", sections=sections)


@app.route("/admin/sections/add", methods=["GET", "POST"])
def add_section():
    if request.method == "POST":
        course_id = request.form["course_ID"]
        section_no = request.form["section_no"]
        semester = request.form["semester"]
        instructor_ID = request.form["instructor_ID"]
        building = request.form["building"]
        room_number = request.form["room_number"]
        timeslot_id = request.form["timeslot_ID"]

        insert_section(course_id, section_no, semester, instructor_ID, building, room_number, timeslot_id)
        return redirect("/admin/sections")

    return render_template("admin/sections/add.html",
        courses=get_all_courses(),
        instructors=get_all_instructors(),
        classrooms=get_all_classrooms(),
        timeslots=get_all_timeslots()
    )


@app.route("/admin/sections/edit/<int:section_id>", methods=["GET", "POST"])
def edit_section(section_id):
    section = get_section_by_id(section_id)

    if request.method == "POST":
        course_id = request.form["course_ID"]
        section_no = request.form["section_no"]
        semester = request.form["semester"]
        instructor_ID = request.form["instructor_ID"]
        building = request.form["building"]
        room_number = request.form["room_number"]
        timeslot_id = request.form["timeslot_ID"]

        update_section(section_id, course_id, section_no, semester, instructor_ID, building, room_number, timeslot_id)
        return redirect("/admin/sections")

    return render_template("admin/sections/edit.html",
        section=section,
        courses=get_all_courses(),
        instructors=get_all_instructors(),
        classrooms=get_all_classrooms(),
        timeslots=get_all_timeslots()
    )


@app.route("/admin/sections/delete/<int:section_id>")
def delete_section_route(section_id):
    delete_section(section_id)
    return redirect("/admin/sections")

####################################
#          CLASSROOMS (ADMIN)
####################################

@app.route("/admin/classrooms")
def admin_classrooms():
    classrooms = get_all_classrooms()
    return render_template("admin/classrooms/list.html", classrooms=classrooms)


@app.route("/admin/classrooms/add", methods=["GET", "POST"])
def add_classroom():
    if request.method == "POST":
        building = request.form["building"]
        room_number = request.form["room_number"]
        capacity = request.form["capacity"]

        insert_classroom(building, room_number, capacity)
        return redirect("/admin/classrooms")

    return render_template("admin/classrooms/add.html")


@app.route("/admin/classrooms/edit/<building>/<room_number>", methods=["GET", "POST"])
def edit_classroom(building, room_number):
    classroom = get_classroom(building, room_number)

    if request.method == "POST":
        new_building = request.form["building"]
        new_room = request.form["room_number"]
        new_capacity = request.form["capacity"]

        update_classroom(building, room_number, new_building, new_room, new_capacity)
        return redirect("/admin/classrooms")

    return render_template("admin/classrooms/edit.html", classroom=classroom)


@app.route("/admin/classrooms/delete/<building>/<room_number>")
def delete_classroom_route(building, room_number):
    delete_classroom(building, room_number)
    return redirect("/admin/classrooms")



####################################
#          TIMESLOTS (ADMIN)
####################################

@app.route("/admin/timeslots")
def admin_timeslots():
    timeslots = get_all_timeslots()
    return render_template("admin/timeslots/list.html", timeslots=timeslots)


@app.route("/admin/timeslots/add", methods=["GET", "POST"])
def add_timeslot():
    if request.method == "POST":
        weekday = request.form["weekday"]
        start_time = request.form["start_time"]
        end_time = request.form["end_time"]

        insert_timeslot(weekday, start_time, end_time)
        return redirect("/admin/timeslots")

    return render_template("admin/timeslots/add.html")


@app.route("/admin/timeslots/edit/<int:timeslot_id>", methods=["GET", "POST"])
def edit_timeslot(timeslot_id):
    timeslot = get_timeslot_by_id(timeslot_id)

    if request.method == "POST":
        weekday = request.form["weekday"]
        start_time = request.form["start_time"]
        end_time = request.form["end_time"]

        update_timeslot(timeslot_id, weekday, start_time, end_time)
        return redirect("/admin/timeslots")

    return render_template("admin/timeslots/edit.html", timeslot=timeslot)


@app.route("/admin/timeslots/delete/<int:timeslot_id>")
def delete_timeslot_route(timeslot_id):
    delete_timeslot(timeslot_id)
    return redirect("/admin/timeslots")


####################################
#         INSTRUCTORS (ADMIN)
####################################

@app.route("/admin/instructors")
def admin_instructors():
    instructors = get_all_instructors()
    return render_template("admin/instructors/list.html", instructors=instructors)


@app.route("/admin/instructors/add", methods=["GET", "POST"])
def add_instructor():
    if request.method == "POST":
        first_name = request.form["first_name"]
        middle_name = request.form["middle_name"]
        last_name = request.form["last_name"]
        email = request.form["email"]
        dept_ID = request.form["dept_ID"]

        insert_instructor(first_name, middle_name, last_name, email, dept_ID)
        return redirect("/admin/instructors")

    departments = get_departments()
    return render_template("admin/instructors/add.html", departments=departments)


@app.route("/admin/instructors/edit/<int:instructor_ID>", methods=["GET", "POST"])
def edit_instructor(instructor_ID):
    instructor = get_instructor_by_id(instructor_ID)

    if request.method == "POST":
        first_name = request.form["first_name"]
        middle_name = request.form["middle_name"]
        last_name = request.form["last_name"]
        email = request.form["email"]
        dept_ID = request.form["dept_ID"]

        update_instructor(instructor_ID, first_name, middle_name, last_name, email, dept_ID)
        return redirect("/admin/instructors")

    departments = get_departments()
    return render_template("admin/instructors/edit.html", instructor=instructor, departments=departments)


@app.route("/admin/instructors/delete/<int:instructor_ID>")
def delete_instructor_route(instructor_ID):
    delete_instructor(instructor_ID)
    return redirect("/admin/instructors")

####################################
#           STUDENTS (ADMIN)


@app.route("/admin/students")
def admin_students():
    students = get_all_students()
    return render_template("admin/students/list.html", students=students)


@app.route("/admin/students/add", methods=["GET", "POST"])
def add_student():
    if request.method == "POST":
        first_name = request.form["first_name"]
        middle_name = request.form["middle_name"]
        last_name = request.form["last_name"]
        email = request.form["email"]
        dept_ID = request.form["dept_ID"]

        insert_student(first_name, middle_name, last_name, email, dept_ID)
        return redirect("/admin/students")

    departments = get_departments()
    return render_template("admin/students/add.html", departments=departments)


@app.route("/admin/students/edit/<int:student_id>", methods=["GET", "POST"])
def edit_student(student_id):
    student = get_student_by_id(student_id)

    if request.method == "POST":
        first_name = request.form["first_name"]
        middle_name = request.form["middle_name"]
        last_name = request.form["last_name"]
        email = request.form["email"]
        dept_ID = request.form["dept_ID"]

        update_student(student_id, first_name, middle_name, last_name, email, dept_ID)
        return redirect("/admin/students")

    departments = get_departments()
    return render_template("admin/students/edit.html", student=student, departments=departments)


@app.route("/admin/students/delete/<int:student_id>")
def delete_student_route(student_id):
    delete_student(student_id)
    return redirect("/admin/students")

#############################################
#   ADMIN — ASSIGN / MODIFY TEACHER TO CLASS


@app.route("/admin/sections/assign/<int:section_id>", methods=["GET", "POST"])
def assign_instructor(section_id):
    section = get_section_by_id(section_id)
    instructors = get_all_instructors()

    if request.method == "POST":
        instructor_id = request.form["instructor_ID"]
        assign_instructor_to_section(section_id, instructor_id)
        return redirect("/admin/sections")

    return render_template(
        "admin/sections/assign.html",
        section=section,
        instructors=instructors
    )

if __name__ == "__main__":
    app.run(debug = True)



