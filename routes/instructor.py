from flask import Blueprint, render_template, request, redirect, url_for,session
from models import *

instructor_bp = Blueprint("instructor", __name__, url_prefix="/instructor")


########################################
#         INSTRUCTOR DASHBOARD
########################################
@instructor_bp.route("/dashboard")
def instructor_dashboard():
    return render_template("instructor/dashboard.html")


########################################
#   SHOW SECTIONS THE INSTRUCTOR TEACHES
########################################
@instructor_bp.route("/grades")
def grade_sections():
    instructor_id = session["instructor_id"]
    sections = get_instructor_sections(instructor_id)

    return render_template(
        "instructor/grades/sections.html",
        sections=sections
    )


########################################
#       SHOW ROSTER FOR ONE SECTION
########################################
@instructor_bp.route("/grades/section/<int:section_id>")
def grade_roster(section_id):

    section = get_section_by_id(section_id)
    roster = get_section_roster(section_id)

    return render_template(
        "instructor/grades/roster.html",
        section=section,
        roster=roster
    )


########################################
#           UPDATE A STUDENT’S GRADE
########################################
@instructor_bp.route("/grades/update", methods=["POST"])
def grade_update():
    enrollment_id = request.form["enrollment_id"]
    grade = request.form["grade"]
    section_id = request.form["section_id"]

    update_grade(enrollment_id, grade)

    # Redirect back to the roster page
    return redirect(url_for("instructor.grade_roster", section_id=section_id))


##########  ADD STUDENTS AS ADVISOR  ##########




@instructor_bp.route("/advisor")
def advisor_students():
    instructor_id = session["instructor_id"]
    students = get_all_students_with_advisors()
    return render_template(
        "instructor/advisor/list.html",
        students=students,
        instructor_id=instructor_id
    )


@instructor_bp.route("/advisor/add/<int:student_id>")
def advisor_add(student_id):
    instructor_id = session["instructor_id"]
    assign_advisor(student_id, instructor_id)
    return redirect("/instructor/advisor")

### 

@instructor_bp.route("/advisor/remove/<int:student_id>")
def advisor_remove(student_id):
    instructor_id = session["instructor_id"]
    remove_advisor(student_id)
    return redirect("/instructor/advisor")

# @instructor_bp.route("/prereq/<int:course_id>")
# def prereq_list(course_id):
#     prereqs = get_prereqs(course_id)
#     all_courses = get_all_courses()
#     return render_template("instructor/prereq/list.html",
#                            course_id=course_id,
#                            prereqs=prereqs,
#                            all_courses=all_courses)


# ## add pre req
# @instructor_bp.route("/prereq/add/<int:course_id>", methods=["POST"])
# def prereq_add(course_id):
#     prereq_id = request.form["prereq_id"]
#     add_prereq(course_id, prereq_id)
#     return redirect(f"/instructor/prereq/{course_id}")

#  # remove re req
# @instructor_bp.route("/prereq/remove/<int:course_id>/<int:prereq_id>")
# def prereq_remove(course_id, prereq_id):
#     remove_prereq(course_id, prereq_id)
#     return redirect(f"/instructor/prereq/{course_id}")

# @instructor_bp.route("/prereq")
# def prereq_courses():
#     instructor_id = 1   # TODO: replace with session login
#     courses = get_instructor_courses(instructor_id)
#     return render_template("instructor/prereq/courses.html", courses=courses)


# --------------------------------
# 1) SHOW COURSES YOU TEACH
# --------------------------------
@instructor_bp.route("/prereq")
def prereq_courses():
    instructor_id = session["instructor_id"]
    courses = get_instructor_courses(instructor_id)
    return render_template("instructor/prereq/courses.html", courses=courses)


# --------------------------------
# 2) SHOW + MANAGE PREREQS FOR ONE COURSE
# --------------------------------
@instructor_bp.route("/prereq/<int:course_id>")
def prereq_list(course_id):
    prereqs = get_prereqs(course_id)
    all_courses = get_all_courses()
    return render_template(
        "instructor/prereq/list.html",
        course_id=course_id,
        prereqs=prereqs,
        all_courses=all_courses,
    )


# --------------------------------
# 3) ADD PREREQUISITE
# --------------------------------
@instructor_bp.route("/prereq/add/<int:course_id>", methods=["POST"])
def prereq_add(course_id):
    prereq_id = request.form["prereq_id"]
    add_prereq(course_id, prereq_id)
    return redirect(f"/instructor/prereq/{course_id}")


# --------------------------------
# 4) REMOVE PREREQUISITE
# --------------------------------
@instructor_bp.route("/prereq/remove/<int:course_id>/<int:prereq_id>")
def prereq_remove(course_id, prereq_id):
    remove_prereq(course_id, prereq_id)
    return redirect(f"/instructor/prereq/{course_id}")

@instructor_bp.route("/grades/remove/<int:enrollment_id>")
def remove_student_from_section(enrollment_id):
    remove_student(enrollment_id)

    # After removing, send instructor back to the roster page
    # We need the section_id to redirect properly
    enrollment = get_enrollment_by_id(enrollment_id)
    section_id = enrollment["section_ID"]

    return redirect(f"/instructor/grades/{section_id}")

def get_enrollment_by_id(enrollment_id):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT * FROM Enrollment WHERE enrollment_ID = %s", (enrollment_id,))
    row = cur.fetchone()
    conn.close()
    return row

def remove_student(enrollment_id):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("DELETE FROM Enrollment WHERE enrollment_ID = %s", (enrollment_id,))
    conn.commit()
    conn.close()

######## Profile #############

@instructor_bp.route("/profile", methods=["GET", "POST"])
def instructor_profile():
    instructor_id = session["instructor_id"]

    instructor = get_instructor(instructor_id)

    message = None

    if request.method == "POST":
        first = request.form["first_name"]
        middle = request.form["middle_name"]
        last = request.form["last_name"]
        email = request.form["email"]

        update_instructor_profile(instructor_id, first, middle, last, email)

        message = "Profile updated successfully!"
        instructor = get_instructor(instructor_id)  # refresh after update

    return render_template(
        "instructor/profile/profile.html",
        instructor=instructor,
        message=message
    )


#### teaching 

@instructor_bp.route("/teaching")
def instructor_teaching():
    instructor_id = session["instructor_id"]
    
    # get all semesters the instructor teaches
    semesters = get_instructor_semesters(instructor_id)

    return render_template("instructor/teaching/choose_semester.html",
                           semesters=semesters)


@instructor_bp.route("/teaching/<semester>")
def instructor_teaching_semester(semester):
    instructor_id = session["instructor_id"]
    
    sections = get_sections_by_semester(instructor_id, semester)

    return render_template("instructor/teaching/list.html",
                           semester=semester,
                           sections=sections)
