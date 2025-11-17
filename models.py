from config import get_connection

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



def get_departments():
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT dept_ID, name FROM Department ORDER BY name")
    rows = cur.fetchall()
    conn.close()
    return rows