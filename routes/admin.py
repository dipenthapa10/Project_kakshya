# routes/admin.py
from flask import Blueprint, render_template, request, redirect, url_for
from models import *
from helper import *

# Create Blueprint
admin_bp = Blueprint("admin", __name__, url_prefix="/admin")

##########################################
#               DASHBOARD
##########################################

@admin_bp.route("/dashboard")
def admin_dashboard():
    return render_template("admin/dashboard.html")


##########################################
#               COURSES CRUD
##########################################

@admin_bp.route("/courses")
def admin_courses():
    data = get_courses()
    return render_template("admin/courses/courses.html", courses=data)

@admin_bp.route("/courses/add", methods=["GET", "POST"])
def add_course():
    if request.method == "POST":
        dept_ID = request.form["dept_ID"]   
        course_no = request.form["course_no"]
        title = request.form["title"]
        credits = request.form["credits"]

        insert_course(dept_ID, course_no, title, credits)
        return redirect("/admin/courses")

    departments = get_departments()
    return render_template("admin/courses/add.html", departments=departments)


@admin_bp.route("/courses/edit/<int:course_id>", methods=["GET", "POST"])
def edit_course(course_id):
    course = get_course_by_id(course_id)
    departments = get_departments()

    if request.method == "POST":
        dept_ID = request.form["dept_ID"]
        course_no = request.form["course_no"]
        title = request.form["title"]
        credits = request.form["credits"]

        update_course(course_id, dept_ID, course_no, title, credits)
        return redirect("/admin/courses")

    return render_template("admin/courses/edit.html", course=course, departments=departments)


@admin_bp.route("/courses/delete/<int:course_id>")
def delete_course_route(course_id):
    delete_course(course_id)
    return redirect("/admin/courses")


##########################################
#           DEPARTMENTS CRUD
##########################################

@admin_bp.route("/departments")
def admin_departments():
    departments = get_all_departments()
    return render_template("admin/departments/list.html", departments=departments)


@admin_bp.route("/departments/add", methods=["GET", "POST"])
def add_department():
    if request.method == "POST":
        name = request.form["name"]
        building = request.form["building"]

        insert_department(name, building)
        return redirect("/admin/departments")

    return render_template("admin/departments/add.html")


@admin_bp.route("/departments/edit/<int:dept_id>", methods=["GET", "POST"])
def edit_department(dept_id):
    department = get_department_by_id(dept_id)

    if request.method == "POST":
        name = request.form["name"]
        building = request.form["building"]

        update_department(dept_id, name, building)
        return redirect("/admin/departments")

    return render_template("admin/departments/edit.html", department=department)


@admin_bp.route("/departments/delete/<int:dept_id>")
def delete_department_route(dept_id):
    delete_department(dept_id)
    return redirect("/admin/departments")


##########################################
#               SECTIONS CRUD
##########################################

@admin_bp.route("/sections")
def admin_sections():
    sections = get_all_sections()
    return render_template("admin/sections/list.html", sections=sections)


# @admin_bp.route("/sections/add", methods=["GET", "POST"])
# def add_section():
#     if request.method == "POST":
#         course_id = request.form["course_ID"]
#         section_no = request.form["section_no"]
#         semester = request.form["semester"]
#         instructor_ID = request.form["instructor_ID"]
#         building = request.form["building"]
#         room_number = request.form["room_number"]
#         timeslot_id = request.form["timeslot_ID"]

#         insert_section(course_id, section_no, semester, instructor_ID, building, room_number, timeslot_id)
#         return redirect("/admin/sections")

#     return render_template(
#         "admin/sections/add.html",
#         courses=get_all_courses(),
#         instructors=get_all_instructors(),
#         classrooms=get_all_classrooms(),
#         timeslots=get_all_timeslots()
#     )

@admin_bp.route("/sections/add", methods=["GET", "POST"])
def add_section():
    if request.method == "POST":
        course_id = request.form["course_ID"]
        section_no = request.form["section_no"]
        semester = request.form["semester"]
        instructor_ID = request.form["instructor_ID"]

        # FIX: Combined classroom value
        classroom = request.form["classroom"]
        building, room_number = classroom.split("|")

        timeslot_id = request.form["timeslot_ID"]

        insert_section(course_id, section_no, semester, instructor_ID, building, room_number, timeslot_id)
        return redirect("/admin/sections")

    return render_template(
        "admin/sections/add.html",
        courses=get_all_courses(),
        instructors=get_all_instructors(),
        classrooms=get_all_classrooms(),
        timeslots=get_all_timeslots()
    )

@admin_bp.route("/sections/edit/<int:section_id>", methods=["GET", "POST"])
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

    return render_template(
        "admin/sections/edit.html",
        section=section,
        courses=get_all_courses(),
        instructors=get_all_instructors(),
        classrooms=get_all_classrooms(),
        timeslots=get_all_timeslots()
    )


@admin_bp.route("/sections/delete/<int:section_id>")
def delete_section_route(section_id):
    delete_section(section_id)
    return redirect("/admin/sections")


##########################################
#              CLASSROOMS CRUD
##########################################

@admin_bp.route("/classrooms")
def admin_classrooms():
    classrooms = get_all_classrooms()
    return render_template("admin/classrooms/list.html", classrooms=classrooms)


@admin_bp.route("/classrooms/add", methods=["GET", "POST"])
def add_classroom():
    if request.method == "POST":
        building = request.form["building"]
        room_number = request.form["room_number"]
        capacity = request.form["capacity"]

        insert_classroom(building, room_number, capacity)
        return redirect("/admin/classrooms")

    return render_template("admin/classrooms/add.html")


@admin_bp.route("/classrooms/edit/<building>/<room_number>", methods=["GET", "POST"])
def edit_classroom(building, room_number):
    # classroom = get_classroom(building, room_number)
    classroom = get_classroom(building, room_number)
   

    if request.method == "POST":
        new_building = request.form["building"]
        new_room = request.form["room_number"]
        new_capacity = request.form["capacity"]

        update_classroom(building, room_number, new_building, new_room, new_capacity)
        return redirect("/admin/classrooms")

    return render_template("admin/classrooms/edit.html", classroom=classroom)


@admin_bp.route("/classrooms/delete/<building>/<room_number>")
def delete_classroom_route(building, room_number):
    delete_classroom(building, room_number)
    return redirect("/admin/classrooms")


##########################################
#                TIMESLOTS CRUD
##########################################

@admin_bp.route("/timeslots")
def admin_timeslots():
    timeslots = get_all_timeslots()
    return render_template("admin/timeslots/list.html", timeslots=timeslots)


@admin_bp.route("/timeslots/add", methods=["GET", "POST"])
def add_timeslot():
    if request.method == "POST":
        weekday = request.form["weekday"]
        start_time = request.form["start_time"]
        end_time = request.form["end_time"]

        insert_timeslot(weekday, start_time, end_time)
        return redirect("/admin/timeslots")

    return render_template("admin/timeslots/add.html")


@admin_bp.route("/timeslots/edit/<int:timeslot_id>", methods=["GET", "POST"])
def edit_timeslot(timeslot_id):
    timeslot = get_timeslot_by_id(timeslot_id)

    if request.method == "POST":
        weekday = request.form["weekday"]
        start_time = request.form["start_time"]
        end_time = request.form["end_time"]

        update_timeslot(timeslot_id, weekday, start_time, end_time)
        return redirect("/admin/timeslots")

    return render_template("admin/timeslots/edit.html", timeslot=timeslot)


@admin_bp.route("/timeslots/delete/<int:timeslot_id>")
def delete_timeslot_route(timeslot_id):
    delete_timeslot(timeslot_id)
    return redirect("/admin/timeslots")


##########################################
#                INSTRUCTORS CRUD
##########################################

@admin_bp.route("/instructors")
def admin_instructors():
    instructors = get_all_instructors()
    return render_template("admin/instructors/list.html", instructors=instructors)




@admin_bp.route("/instructors/add", methods=["GET", "POST"])
def add_instructor():
    if request.method == "POST":
        first_name = request.form["first_name"]
        middle_name = request.form["middle_name"]
        last_name = request.form["last_name"]
        email = request.form["email"]
        dept_ID = request.form["dept_ID"]

        insert_instructor(first_name, middle_name, last_name, email, dept_ID)
        return redirect("/admin/instructors")

    return render_template("admin/instructors/add.html", departments=get_departments())


@admin_bp.route("/instructors/edit/<int:instructor_ID>", methods=["GET", "POST"])
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

    return render_template("admin/instructors/edit.html", instructor=instructor, departments=get_departments())


@admin_bp.route("/instructors/delete/<int:instructor_ID>")
def delete_instructor_route(instructor_ID):
    delete_instructor(instructor_ID)
    return redirect("/admin/instructors")

##########################################
#                 STUDENTS CRUD
##########################################

@admin_bp.route("/students")
def admin_students():
    students = get_all_students()
    return render_template("admin/students/list.html", students=students)


@admin_bp.route("/students/add", methods=["GET", "POST"])
def add_student():
    if request.method == "POST":
        first_name = request.form["first_name"]
        middle_name = request.form["middle_name"]
        last_name = request.form["last_name"]
        email = request.form["email"]
        dept_ID = request.form["dept_ID"]

        insert_student(first_name, middle_name, last_name, email, dept_ID)
        return redirect("/admin/students")

    return render_template("admin/students/add.html", departments=get_departments())


@admin_bp.route("/students/edit/<int:student_id>", methods=["GET", "POST"])
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

    return render_template("admin/students/edit.html", student=student, departments=get_departments())


@admin_bp.route("/students/delete/<int:student_id>")
def delete_student_route(student_id):
    delete_student(student_id)
    return redirect("/admin/students")


##########################################
#     ASSIGN / MODIFY / REMOVE TEACHER
##########################################

@admin_bp.route("/sections/assign/<int:section_id>", methods=["GET", "POST"])
def assign_instructor(section_id):
    section = get_section_by_id(section_id)
    instructors = get_all_instructors()

    if request.method == "POST":
        instructor_id = request.form["instructor_ID"]
        assign_instructor_to_section(section_id, instructor_id)
        return redirect("/admin/sections")

    return render_template("admin/sections/assign.html", section=section, instructors=instructors)


@admin_bp.route("/sections/remove-teacher/<int:section_id>")
def remove_teacher_route(section_id):
    remove_teacher(section_id)
    return redirect("/admin/sections")

