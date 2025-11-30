from config import get_connection
############# ADMIN ###########
################################


####################### COURSE ############################ 


### READ ALL ###
def get_courses():
    conn = get_connection()
    cur = conn.cursor() 
    cur.execute("SELECT * FROM Course")
    rows = cur.fetchall()
    conn.close()
    return rows

### READ ONE ###
def get_course_by_id(course_id):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT * FROM Course WHERE course_ID = %s", (course_id,))
    row = cur.fetchone()
    conn.close()
    return row


### CREATE ###
def insert_course(name, course_no, title, credits):
    conn = get_connection()
    cur = conn.cursor()

    # Get dept_ID from Department table using the department name
    cur.execute("SELECT dept_ID FROM Department WHERE name = %s", (name,))
    result = cur.fetchone()

    if not result:
        print("Department does not exist.")
        conn.close()
        return

    dept_ID = result["dept_ID"]  # because you're using DictCursor

    # Now insert course
    cur.execute("""
        INSERT INTO Course (dept_ID, course_no, title, credits)
        VALUES (%s, %s, %s, %s)
    """, (dept_ID, course_no, title, credits))

    conn.commit()
    conn.close()



### UPDATE ###
def update_course(course_id, dept_ID, course_no, title, credits):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("""
        UPDATE Course
        SET dept_ID=%s, course_no=%s, title=%s, credits=%s
        WHERE course_ID = %s
    """, (dept_ID, course_no, title, credits, course_id))
    conn.commit()
    conn.close()


### DELETE ###
def delete_course(course_id):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("DELETE FROM Course WHERE course_ID = %s", (course_id,))
    conn.commit()
    conn.close()

####################### DEPARTMENT ############################

# for dropdown
def get_departments():
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT dept_ID, name FROM Department ORDER BY name")
    rows = cur.fetchall()
    conn.close()
    return rows

# READ ALL
def get_all_departments():
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT * FROM Department")
    rows = cur.fetchall()
    conn.close()
    return rows


# READ ONE
def get_department_by_id(dept_id):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT * FROM Department WHERE dept_ID = %s", (dept_id,))
    row = cur.fetchone()
    conn.close()
    return row


# CREATE
def insert_department(name, building):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("""
        INSERT INTO Department (name, building)
        VALUES (%s, %s)
    """, (name, building))
    conn.commit()
    conn.close()


# UPDATE
def update_department(dept_id, name, building):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("""
        UPDATE Department
        SET name=%s, building=%s
        WHERE dept_ID = %s
    """, (name, building, dept_id))
    conn.commit()
    conn.close()


# DELETE
def delete_department(dept_id):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("DELETE FROM Department WHERE dept_ID = %s", (dept_id,))
    conn.commit()
    conn.close()


################ CRUD SECTION ################



def get_all_sections():
    conn = get_connection()
    cur = conn.cursor()
    
    cur.execute("""
        SELECT 
            s.section_ID, s.course_ID, s.section_no, s.semester,
            s.instructor_ID, s.building, s.room_number, s.timeslot_ID,
            c.course_no, c.title,
            i.first_name, i.last_name,
            t.weekday, t.start_time, t.end_time
        FROM Section s
        JOIN Course c ON s.course_ID = c.course_ID
        LEFT JOIN Instructor i ON s.instructor_ID = i.instructor_ID   -- FIX
        JOIN Timeslot t ON s.timeslot_ID = t.timeslot_ID
        ORDER BY s.section_ID
    """)
    
    results = cur.fetchall()
    conn.close()
    return results


#read one section 
def get_section_by_id(section_id):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT * FROM Section WHERE section_ID = %s", (section_id,))
    row = cur.fetchone()
    conn.close()
    return row

# create section

def insert_section(course_ID, section_no, semester, instructor_ID, building, room_number, timeslot_ID):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("""
        INSERT INTO Section (course_ID, section_no, semester, instructor_ID, building, room_number, timeslot_ID)
        VALUES (%s, %s, %s, %s, %s, %s, %s)
    """, (course_ID, section_no, semester, instructor_ID, building, room_number, timeslot_ID))
    conn.commit()
    conn.close()

#update section 
def update_section(section_id, course_ID, section_no, semester, instructor_ID, building, room_number, timeslot_ID):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("""
        UPDATE Section
        SET course_ID=%s, section_no=%s, semester=%s, instructor_ID=%s,
            building=%s, room_number=%s, timeslot_ID=%s
        WHERE section_ID = %s
    """, (course_ID, section_no, semester, instructor_ID, building, room_number, timeslot_ID, section_id))
    conn.commit()
    conn.close()

#delete section 
def delete_section(section_id):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("DELETE FROM Section WHERE section_ID = %s", (section_id,))
    conn.commit()
    conn.close()


# =====================================
#        CLASSROOM CRUD


def get_all_classrooms():
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT * FROM Classroom ORDER BY building, room_number")
    rows = cur.fetchall()
    conn.close()
    return rows


def get_classroom(building, room_number):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("""
        SELECT * FROM Classroom
        WHERE building = %s AND room_number = %s
    """, (building, room_number))
    row = cur.fetchone()
    conn.close()
    return row


def insert_classroom(building, room_number, capacity):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("""
        INSERT INTO Classroom (building, room_number, capacity)
        VALUES (%s, %s, %s)
    """, (building, room_number, capacity))
    conn.commit()
    conn.close()


def update_classroom(old_building, old_room, building, room_number, capacity):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("""
        UPDATE Classroom
        SET building = %s, room_number = %s, capacity = %s
        WHERE building = %s AND room_number = %s
    """, (building, room_number, capacity, old_building, old_room))
    conn.commit()
    conn.close()


def delete_classroom(building, room_number):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("""
        DELETE FROM Classroom
        WHERE building = %s AND room_number = %s
    """, (building, room_number))
    conn.commit()
    conn.close()



#            TIMESLOT CRUD


def get_all_timeslots():
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT * FROM Timeslot ORDER BY timeslot_ID")
    rows = cur.fetchall()
    conn.close()
    return rows


def get_timeslot_by_id(timeslot_id):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT * FROM Timeslot WHERE timeslot_ID = %s", (timeslot_id,))
    row = cur.fetchone()
    conn.close()
    return row


def insert_timeslot(weekday, start_time, end_time):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("""
        INSERT INTO Timeslot (weekday, start_time, end_time)
        VALUES (%s, %s, %s)
    """, (weekday, start_time, end_time))
    conn.commit()
    conn.close()


def update_timeslot(timeslot_id, weekday, start_time, end_time):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("""
        UPDATE Timeslot
        SET weekday=%s, start_time=%s, end_time=%s
        WHERE timeslot_ID=%s
    """, (weekday, start_time, end_time, timeslot_id))
    conn.commit()
    conn.close()


def delete_timeslot(timeslot_id):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("DELETE FROM Timeslot WHERE timeslot_ID=%s", (timeslot_id,))
    conn.commit()
    conn.close()


# =====================================
#            INSTRUCTOR CRUD


def get_all_instructors():
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("""
        SELECT i.instructor_ID, i.first_name, i.middle_name, i.last_name, 
               i.email, d.name AS dept_name
        FROM Instructor i
        JOIN Department d ON i.dept_ID = d.dept_ID
        ORDER BY i.last_name
    """)
    rows = cur.fetchall()
    conn.close()
    return rows


def get_instructor_by_id(instructor_ID):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT * FROM Instructor WHERE instructor_ID = %s", (instructor_ID,))
    row = cur.fetchone()
    conn.close()
    return row


def insert_instructor(first_name, middle_name, last_name, email, dept_ID):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("""
        INSERT INTO Instructor (first_name, middle_name, last_name, email, dept_ID)
        VALUES (%s, %s, %s, %s, %s)
    """, (first_name, middle_name, last_name, email, dept_ID))
    conn.commit()
    conn.close()


def update_instructor(instructor_ID, first_name, middle_name, last_name, email, dept_ID):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("""
        UPDATE Instructor
        SET first_name=%s, middle_name=%s, last_name=%s, email=%s, dept_ID=%s
        WHERE instructor_ID=%s
    """, (first_name, middle_name, last_name, email, dept_ID, instructor_ID))
    conn.commit()
    conn.close()


def delete_instructor(instructor_ID):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("DELETE FROM Instructor WHERE instructor_ID=%s", (instructor_ID,))
    conn.commit()
    conn.close()


# =====================================
#             STUDENT CRUD


def get_all_students():
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("""
        SELECT s.student_ID, s.first_name, s.middle_name, s.last_name, 
               s.email, d.name AS dept_name
        FROM Student s
        JOIN Department d ON s.dept_ID = d.dept_ID
        ORDER BY s.last_name
    """)
    rows = cur.fetchall()
    conn.close()
    return rows


def get_student_by_id(student_id):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT * FROM Student WHERE student_ID = %s", (student_id,))
    row = cur.fetchone()
    conn.close()
    return row


def insert_student(first_name, middle_name, last_name, email, dept_ID):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("""
        INSERT INTO Student (first_name, middle_name, last_name, email, dept_ID)
        VALUES (%s, %s, %s, %s, %s)
    """, (first_name, middle_name, last_name, email, dept_ID))
    conn.commit()
    conn.close()


def update_student(student_id, first_name, middle_name, last_name, email, dept_ID):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("""
        UPDATE Student
        SET first_name=%s, middle_name=%s, last_name=%s, email=%s, dept_ID=%s
        WHERE student_ID=%s
    """, (first_name, middle_name, last_name, email, dept_ID, student_id))
    conn.commit()
    conn.close()


def delete_student(student_id):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("DELETE FROM Student WHERE student_ID=%s", (student_id,))
    conn.commit()
    conn.close()

## assign
def assign_instructor_to_section(section_id, instructor_ID):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("""
        UPDATE Section
        SET instructor_ID = %s
        WHERE section_ID = %s
    """, (instructor_ID, section_id))
    conn.commit()
    conn.close()

def remove_teacher(section_id):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("""
        UPDATE Section
        SET instructor_ID = NULL
        WHERE section_ID = %s
    """, (section_id,))
    conn.commit()
    conn.close()

########### Instructor################

#### get section taught by insttructor 

def get_instructor_sections(instructor_id):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("""
        SELECT s.section_ID, s.section_no, s.semester, c.course_no, c.title
        FROM Section s
        JOIN Course c ON s.course_ID = c.course_ID
        WHERE s.instructor_ID = %s
    """, (instructor_id,))
    rows = cur.fetchall()
    conn.close()
    return rows


##### Get roster of a section
def get_section_roster(section_id):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("""
        SELECT e.enrollment_ID, st.student_ID, st.first_name, st.last_name, e.grade
        FROM Enrollment e
        JOIN Student st ON e.student_ID = st.student_ID
        WHERE e.section_ID = %s
    """, (section_id,))
    rows = cur.fetchall()
    conn.close()
    return rows

## update grade 

def update_grade(enrollment_id, grade):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("""
        UPDATE Enrollment
        SET grade = %s
        WHERE enrollment_ID = %s
    """, (grade, enrollment_id))
    conn.commit()
    conn.close()


########## Add students as advisor #############

def get_students_without_advisor():
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("""
        SELECT student_ID, first_name, last_name, email 
        FROM Student
        WHERE advisor_ID IS NULL
        ORDER BY last_name
    """)
    rows = cur.fetchall()
    conn.close()
    return rows


def assign_advisor(student_id, instructor_id):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("""
        UPDATE Student
        SET advisor_ID = %s
        WHERE student_ID = %s
    """, (instructor_id, student_id))
    conn.commit()
    conn.close()


def get_all_students_with_advisors():
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("""
        SELECT 
            s.student_ID,
            s.first_name,
            s.last_name,
            s.email,
            s.advisor_ID
        FROM Student s
        ORDER BY s.last_name
    """)
    rows = cur.fetchall()
    conn.close()
    return rows

### Remove as advisor

def remove_advisor(student_id):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("""
        UPDATE Student
        SET advisor_ID = NULL
        WHERE student_ID = %s
    """, (student_id,))
    conn.commit()
    conn.close()

#### pre req 

# def get_prereqs(course_id):
#     conn = get_connection()
#     cur = conn.cursor()
#     cur.execute("""
#         SELECT P.prereq_course_ID, C.course_no, C.title
#         FROM Pre_Requisite P
#         JOIN Course C ON P.prereq_course_ID = C.course_ID
#         WHERE P.course_ID = %s
#     """, (course_id,))
#     rows = cur.fetchall()
#     conn.close()
#     return rows

# ## insert pre req 

# def add_prereq(course_id, prereq_id):
#     conn = get_connection()
#     cur = conn.cursor()
#     cur.execute("""
#         INSERT INTO Pre_Requisite (course_ID, prereq_course_ID, prereq_title)
#         SELECT %s, course_ID, title
#         FROM Course
#         WHERE course_ID = %s
#     """, (course_id, prereq_id))
#     conn.commit()
#     conn.close()

#     ## delete 
# def remove_prereq(course_id, prereq_id):
#     conn = get_connection()
#     cur = conn.cursor()
#     cur.execute("""
#         DELETE FROM Pre_Requisite
#         WHERE course_ID = %s AND prereq_course_ID = %s
#     """, (course_id, prereq_id))
#     conn.commit()
#     conn.close()


# def get_instructor_courses(instructor_id):
#     conn = get_connection()
#     cur = conn.cursor()
#     cur.execute("""
#         SELECT C.course_ID, C.course_no, C.title
#         FROM Section S
#         JOIN Course C ON S.course_ID = C.course_ID
#         WHERE S.instructor_ID = %s
#         GROUP BY C.course_ID
#     """, (instructor_id,))
#     rows = cur.fetchall()
#     conn.close()
#     return rows

# -------------------------------
# PREREQUISITE FUNCTIONS
# -------------------------------

def get_prereqs(course_id):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("""
        SELECT P.prereq_course_ID, C.course_no, C.title
        FROM Pre_Requisite P
        JOIN Course C ON P.prereq_course_ID = C.course_ID
        WHERE P.course_ID = %s
    """, (course_id,))
    rows = cur.fetchall()
    conn.close()
    return rows


def add_prereq(course_id, prereq_id):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("""
        INSERT INTO Pre_Requisite (course_ID, prereq_course_ID)
        VALUES (%s, %s)
    """, (course_id, prereq_id))
    conn.commit()
    conn.close()


def remove_prereq(course_id, prereq_id):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("""
        DELETE FROM Pre_Requisite
        WHERE course_ID = %s AND prereq_course_ID = %s
    """, (course_id, prereq_id))
    conn.commit()
    conn.close()


def get_instructor_courses(instructor_id):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("""
        SELECT C.course_ID, C.course_no, C.title
        FROM Section S
        JOIN Course C ON S.course_ID = C.course_ID
        WHERE S.instructor_ID = %s
        GROUP BY C.course_ID
    """, (instructor_id,))
    rows = cur.fetchall()
    conn.close()
    return rows

def get_all_courses():
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT * FROM Course ORDER BY course_no")
    rows = cur.fetchall()
    conn.close()
    return rows

########## Profile #######

def update_instructor_profile(instructor_id, first, middle, last, email):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("""
        UPDATE Instructor
        SET first_name = %s, middle_name = %s, last_name = %s, email = %s
        WHERE instructor_ID = %s
    """, (first, middle, last, email, instructor_id))
    conn.commit()
    conn.close()



def get_instructor(instructor_id):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("""
        SELECT instructor_ID, first_name, middle_name, last_name, email
        FROM Instructor
        WHERE instructor_ID = %s
    """, (instructor_id,))
    row = cur.fetchone()
    conn.close()
    return row


#### get available 

def get_instructor_semesters(instructor_id):
    conn = get_connection()
    cur = conn.cursor()
    
    cur.execute("""
        SELECT DISTINCT semester
        FROM Section
        WHERE instructor_ID = %s
        ORDER BY semester
    """, (instructor_id,))
    
    rows = cur.fetchall()
    conn.close()
    return rows

## get section by sem

def get_sections_by_semester(instructor_id, semester):
    conn = get_connection()
    cur = conn.cursor()
    
    cur.execute("""
        SELECT S.section_ID, S.section_no, S.semester,
               C.course_no, C.title
        FROM Section S
        JOIN Course C ON S.course_ID = C.course_ID
        WHERE S.instructor_ID = %s AND S.semester = %s
    """, (instructor_id, semester))
    
    rows = cur.fetchall()
    conn.close()
    return rows


##################### #########
####### STUDENT ###############
##########

def get_student_enrollments(student_id):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("""
        SELECT section_ID
        FROM Enrollment
        WHERE student_ID = %s
    """, (student_id,))
    rows = cur.fetchall()
    conn.close()
    return rows


def register_student_in_section(student_id, section_id):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("""
        INSERT INTO Enrollment(student_ID, section_ID, enroll_semester, enroll_year)
        VALUES (%s, %s, 'Fall', 2025)
    """, (student_id, section_id))
    conn.commit()
    conn.close()

def drop_student_from_section(student_id, section_id):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("""
        DELETE FROM Enrollment
        WHERE student_ID = %s AND section_ID = %s
    """, (student_id, section_id))
    conn.commit()
    conn.close()



def get_all_sections():
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("""
        SELECT S.section_ID, S.section_no, S.semester,
               C.course_no, C.title,
               I.first_name, I.last_name
        FROM Section S
        JOIN Course C ON S.course_ID = C.course_ID
        LEFT JOIN Instructor I ON S.instructor_ID = I.instructor_ID
    """)
    rows = cur.fetchall()
    conn.close()
    return rows


#### drop 

def drop_student_class(student_id, section_id):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("""
        DELETE FROM Enrollment
        WHERE student_ID = %s AND section_ID = %s
    """, (student_id, section_id))
    conn.commit()
    conn.close()




#### check final grades 

def get_student_grades(student_id):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("""
        SELECT 
            C.course_no,
            C.title,
            S.section_no,
            S.semester,
            E.grade
        FROM Enrollment E
        JOIN Section S ON E.section_ID = S.section_ID
        JOIN Course C ON S.course_ID = C.course_ID
        WHERE E.student_ID = %s
    """, (student_id,))
    
    rows = cur.fetchall()
    conn.close()
    return rows

## Get all semesters a student has
def get_student_semesters(student_id):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("""
        SELECT DISTINCT S.semester
        FROM Enrollment E
        JOIN Section S ON E.section_ID = S.section_ID
        WHERE E.student_ID = %s
        ORDER BY S.semester
    """, (student_id,))
    rows = cur.fetchall()
    conn.close()
    return [row['semester'] for row in rows]

## get courses by sememster

def get_courses_by_semester(student_id, semester):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("""
        SELECT
            C.course_no,
            C.title,
            S.section_no,
            S.semester,
            E.grade,
            CASE
                WHEN E.grade IS NULL AND S.semester = %s THEN 'In Progress'
                WHEN E.grade IS NULL AND S.semester < %s THEN 'Completed (Missing Grade)'
                WHEN E.grade IS NULL THEN 'Not Started'
                ELSE 'Completed'
            END AS status
        FROM Enrollment E
        JOIN Section S ON E.section_ID = S.section_ID
        JOIN Course C ON S.course_ID = C.course_ID
        WHERE E.student_ID = %s AND S.semester = %s
        ORDER BY C.course_no
    """, (semester, semester, student_id, semester))

    rows = cur.fetchall()
    conn.close()
    return rows


### full section details

def get_section_info(section_id):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("""
        SELECT 
            S.section_ID,
            S.section_no,
            S.semester,
            C.course_ID,
            C.course_no,
            C.title,
            C.credits,
            I.first_name,
            I.last_name,
            CL.building,
            CL.room_number,
            T.weekday,
            T.start_time,
            T.end_time
        FROM Section S
        JOIN Course C ON S.course_ID = C.course_ID
        LEFT JOIN Instructor I ON S.instructor_ID = I.instructor_ID
        LEFT JOIN Classroom CL ON S.building = CL.building AND S.room_number = CL.room_number
        LEFT JOIN Timeslot T ON S.timeslot_ID = T.timeslot_ID
        WHERE S.section_ID = %s
    """, (section_id,))
    row = cur.fetchone()
    conn.close()
    return row

## get pre req foor the course 

def get_course_prereqs(course_id):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("""
        SELECT C.course_no, C.title
        FROM Pre_Requisite P
        JOIN Course C ON P.prereq_course_ID = C.course_ID
        WHERE P.course_ID = %s
    """, (course_id,))
    rows = cur.fetchall()
    conn.close()
    return rows

## check student if enrolled 

def is_student_enrolled(student_id, section_id):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("""
        SELECT 1
        FROM Enrollment
        WHERE student_ID = %s AND section_ID = %s
    """, (student_id, section_id))
    row = cur.fetchone()
    conn.close()
    return row is not None



def get_student_sections(student_id):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("""
        SELECT 
            E.section_ID,
            S.section_no,
            S.semester,
            C.course_no,
            C.title
        FROM Enrollment E
        JOIN Section S ON E.section_ID = S.section_ID
        JOIN Course C ON S.course_ID = C.course_ID
        WHERE E.student_ID = %s
    """, (student_id,))
    rows = cur.fetchall()
    conn.close()
    return rows


###### advisor part

def get_student_advisor(student_id):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("""
        SELECT 
            I.instructor_ID,
            I.first_name,
            I.last_name,
            I.email,
            D.name AS dept_name
        FROM Advisor A
        JOIN Instructor I ON A.instructor_ID = I.instructor_ID
        JOIN Department D ON I.dept_ID = D.dept_ID
        WHERE A.student_ID = %s
    """, (student_id,))
    row = cur.fetchone()
    conn.close()
    return row


#### profile

def get_student(student_id):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("""
        SELECT student_ID, first_name, middle_name, last_name, email
        FROM Student
        WHERE student_ID = %s
    """, (student_id,))
    row = cur.fetchone()
    conn.close()
    return row

def update_student_profile(student_id, first, middle, last, email):

    if middle.strip() == "":
        middle = None
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("""
        UPDATE Student
        SET first_name = %s,
            middle_name = %s,
            last_name = %s,
            email = %s
        WHERE student_ID = %s
    """, (first, middle, last, email, student_id))
    conn.commit()
    conn.close()

