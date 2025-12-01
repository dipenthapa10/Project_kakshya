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
#   SHOW SECTIONS PAGE (Your Sections)
########################################
@instructor_bp.route("/sections")
def instructor_sections():
    instructor_id = session["instructor_id"]

    # Reuse the same query used by /grades
    sections = get_instructor_sections(instructor_id)

    return render_template(
        "instructor/sections/list.html",
        sections=sections
    )


@instructor_bp.route("/sections/roster/<int:section_id>")
def section_roster(section_id):
    section = get_section_by_id(section_id)
    roster = get_section_roster(section_id)

    return render_template(
        "instructor/sections/roster.html",
        section=section,
        roster=roster
    )

##### 

@instructor_bp.route("/sections/remove/<int:section_id>")
def section_remove(section_id):
    section = get_section_by_id(section_id)
    roster = get_section_roster(section_id)

    return render_template(
        "instructor/sections/remove.html",
        section=section,
        roster=roster
    )

@instructor_bp.route("/sections/remove/student/<int:enrollment_id>")
def remove_student_from_section(enrollment_id):

    enrollment = get_enrollment_by_id(enrollment_id)
    section_id = enrollment["section_ID"]

    remove_student(enrollment_id)

    return redirect(f"/instructor/sections/remove/{section_id}")



########################################
#   SHOW SECTIONS THE INSTRUCTOR TEACHES
########################################
@instructor_bp.route("/grades")
def grade_sections():
    instructor_id = session["instructor_id"]
    sections = get_instructor_sections(instructor_id)

    return render_template(
        "instructor/grades/grades.html",
        sections=sections
    )

# ########################################
# #  SHOW SECTIONS FOR GRADING
# ########################################
# @instructor_bp.route("/grades")
# def grades_home():
#     instructor_id = session["instructor_id"]
#     sections = get_instructor_sections(instructor_id)

#     return render_template(
#         "instructor/grades/grades.html",
#         sections=sections
#     )


########################################
#  SHOW ROSTER FOR ONE SECTION (GRADE VIEW)
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
#  SUBMIT / CHANGE A STUDENT’S GRADE
########################################
@instructor_bp.route("/grades/update", methods=["POST"])
def grade_update():
    enrollment_id = request.form["enrollment_id"]
    grade = request.form["grade"]
    section_id = request.form["section_id"]

    update_grade(enrollment_id, grade)

    return redirect(f"/instructor/grades/section/{section_id}")



########################################
#           UPDATE A STUDENT’S GRADE
########################################
# @instructor_bp.route("/grades/update", methods=["POST"])
# def grade_update():
#     enrollment_id = request.form["enrollment_id"]
#     grade = request.form["grade"]
#     section_id = request.form["section_id"]

#     update_grade(enrollment_id, grade)

#     # Redirect back to the roster page
#     return redirect(url_for("instructor.grade_roster", section_id=section_id))







######################################################################



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

# @instructor_bp.route("/grades/remove/<int:enrollment_id>")
# def remove_student_from_section(enrollment_id):
#     remove_student(enrollment_id)

#     # After removing, send instructor back to the roster page
#     # We need the section_id to redirect properly
#     enrollment = get_enrollment_by_id(enrollment_id)
#     section_id = enrollment["section_ID"]

#     return redirect(f"/instructor/grades/{section_id}")

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



################################
##     FINAL HW5
#######


@instructor_bp.route("/analytics/department_averages")
def department_averages():
    dept_stats = get_avg_grade_by_department()
    return render_template(
        "instructor/analytics/department_averages.html",
        dept_stats=dept_stats
    )


#### Give the average grade of a class across a range of semesters (selected by the user).

@instructor_bp.route("/analytics/class_average", methods=["GET", "POST"])
def class_average():
    instructor_id = session["instructor_id"]

    # Get courses the instructor teaches
    courses = get_instructor_courses(instructor_id)

    # If user submitted the form
    if request.method == "POST":
        course_id = request.form["course_id"]
        sem_start = request.form["sem_start"]
        sem_end = request.form["sem_end"]

        avg = get_class_average(course_id, sem_start, sem_end)

        return render_template(
            "instructor/analytics/class_average_result.html",
            avg=avg,
            sem_start=sem_start,
            sem_end=sem_end
        )

    # Otherwise show selection form
    return render_template(
        "instructor/analytics/class_average_form.html",
        courses=courses
    )

### Show the best and worst performing classes (based on grades) for a selected semester.

@instructor_bp.route("/analytics/best-worst")
def best_worst_class():
    semesters = get_all_semesters()  # We'll create this function
    return render_template(
        "instructor/analytics/choose_semester_best_worst.html",
        semesters=semesters
    )

@instructor_bp.route("/analytics/best-worst/results", methods=["POST"])
def best_worst_results():
    semester = request.form["semester"]

    results = get_best_and_worst_classes(semester)

    return render_template(
        "instructor/analytics/best_worst_results.html",
        semester=semester,
        results=results
    )

## Show the total number of students (past and current) according to the department.

@instructor_bp.route("/analytics/student_counts")
def student_counts():
    data = get_student_count_by_department()
    return render_template(
        "instructor/analytics/student_counts.html",
        data=data
    )

# Show the total number of students currently enrolled according to the department.

@instructor_bp.route("/analytics/current_enrollment")
def current_enrollment():
    data = get_current_enrollment_by_department()
    return render_template(
        "instructor/analytics/current_enrollment.html",
        data=data
    )
