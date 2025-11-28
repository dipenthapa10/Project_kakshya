# ---- Student routes ----
# Put this near your admin routes, AFTER `app = Flask(__name__)`
# and after your DB config/imports

from flask import render_template, request, redirect, url_for, session
from db.student_queries import (
    get_student_by_id,
    get_student_courses,
    get_student_grades,
    get_course_detail,
)

def get_current_student_id():
    """
    Helper to get the currently 'logged in' student.
    For now, if no session id is set, it falls back to a demo student.
    You can replace this later when you add real login.
    """
    student_id = session.get("student_id")
    if not student_id:
        # TEMP: default student for demo/testing
        student_id = "001"
    return student_id


@app.route("/student/dashboard")
def student_dashboard():
    student_id = get_current_student_id()
    student = get_student_by_id(student_id)
    courses = get_student_courses(student_id)

    return render_template(
        "student/dashboard.html",
        student=student,
        courses=courses,
    )


@app.route("/student/courses")
def student_courses():
    student_id = get_current_student_id()
    courses = get_student_courses(student_id)

    return render_template(
        "student/courses.html",
        courses=courses,
    )


@app.route("/student/grades")
def student_grades():
    student_id = get_current_student_id()
    grades = get_student_grades(student_id)

    return render_template(
        "student/grades.html",
        grades=grades,
    )


@app.route("/student/profile")
def student_profile():
    student_id = get_current_student_id()
    student = get_student_by_id(student_id)

    return render_template(
        "student/profile.html",
        student=student,
    )


@app.route("/student/course/<int:course_id>")
def student_course_detail(course_id):
    student_id = get_current_student_id()
    course = get_course_detail(course_id)

    return render_template(
        "student/course_detail.html",
        course=course,
    )


@app.route("/student/logout")
def student_logout():
    # Clear only the student session (keep it simple)
    session.pop("student_id", None)
    return redirect(url_for("home"))
