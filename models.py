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


