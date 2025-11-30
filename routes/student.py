from flask import Blueprint, render_template, request, redirect, session
from models import *

student_bp = Blueprint("student", __name__, url_prefix="/student")


# -------------- Helper: require student login --------------
def require_student():
    if session.get("role") != "student":
        return False
    return session.get("student_id")


# ------------------------------
# STUDENT DASHBOARD
# ------------------------------
@student_bp.route("/dashboard")
def dashboard():
    student_id = require_student()
    if not student_id:
        return redirect("/auth/login")

    enrolled_sections = get_student_sections(student_id)

    return render_template("student/dashboard.html",
                           enrolled_sections=enrolled_sections)


# ------------------------------
# REGISTER / DROP
# ------------------------------
@student_bp.route("/register")
def register_page():
    student_id = require_student()
    if not student_id:
        return redirect("/auth/login")

    sections = get_all_sections()
    enrolled = get_student_enrollments(student_id)
    enrolled_ids = [s['section_ID'] for s in enrolled]

    return render_template("student/register/list.html",
                           sections=sections,
                           enrolled_ids=enrolled_ids)


@student_bp.route("/register/<int:section_id>")
def register_action(section_id):
    student_id = require_student()
    if not student_id:
        return redirect("/auth/login")

    register_student_in_section(student_id, section_id)
    return redirect("/student/register")


@student_bp.route("/drop/<int:section_id>")
def drop_class(section_id):
    student_id = require_student()
    if not student_id:
        return redirect("/auth/login")

    drop_student_class(student_id, section_id)
    return redirect("/student/register")


# ------------------------
# VIEW FINAL GRADES
# ------------------------
@student_bp.route("/grades")
def view_grades():
    student_id = require_student()
    if not student_id:
        return redirect("/auth/login")

    grades = get_student_grades(student_id)
    return render_template("student/grades.html", grades=grades)


# ------------------------------
# COURSES BY SEMESTER
# ------------------------------
@student_bp.route("/semesters")
def student_semesters():
    student_id = require_student()
    if not student_id:
        return redirect("/auth/login")

    semesters = get_student_semesters(student_id)
    return render_template("student/semesters.html", semesters=semesters)


@student_bp.route("/semesters/<string:semester>")
def student_semester_courses(semester):
    student_id = require_student()
    if not student_id:
        return redirect("/auth/login")

    courses = get_courses_by_semester(student_id, semester)
    return render_template("student/semester_courses.html",
                           semester=semester,
                           courses=courses)


# ------------------------------
# SECTION INFO PAGE
# ------------------------------
@student_bp.route("/section_info/<int:section_id>")
def section_info(section_id):
    student_id = require_student()
    if not student_id:
        return redirect("/auth/login")

    section = get_section_info(section_id)
    prereqs = get_course_prereqs(section["course_ID"])
    enrolled = is_student_enrolled(student_id, section_id)

    return render_template("student/section_info.html",
                           section=section,
                           prereqs=prereqs,
                           enrolled=enrolled)


# ------------------------------
# SECTION SELECT
# ------------------------------
@student_bp.route("/section_select")
def section_select():
    student_id = require_student()
    if not student_id:
        return redirect("/auth/login")

    sections = get_student_sections(student_id)
    return render_template("student/section_select.html", sections=sections)


# ------------------------------
# ADVISOR
# ------------------------------
@student_bp.route("/advisor")
def advisor_info():
    student_id = require_student()
    if not student_id:
        return redirect("/auth/login")

    advisor = get_student_advisor(student_id)
    return render_template("student/advisor.html", advisor=advisor)


# ------------------------------
# PROFILE
# ------------------------------
@student_bp.route("/profile", methods=["GET", "POST"])
def student_profile():
    student_id = require_student()
    if not student_id:
        return redirect("/auth/login")

    if request.method == "POST":
        first = request.form["first_name"]
        middle = request.form["middle_name"]
        last = request.form["last_name"]
        email = request.form["email"]

        update_student_profile(student_id, first, middle, last, email)

        return render_template("student/profile.html",
                               student=get_student(student_id),
                               msg="Profile updated successfully!")

    student = get_student(student_id)
    return render_template("student/profile.html", student=student)

