
### contains dropwdowns

from config import get_connection

def get_all_courses():
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT course_ID, course_no, title FROM Course ORDER BY course_no")
    rows = cur.fetchall()
    conn.close()
    return rows

def get_all_instructors():
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT instructor_ID, first_name, last_name FROM Instructor ORDER BY last_name")
    rows = cur.fetchall()
    conn.close()
    return rows

def get_all_classrooms():
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT building, room_number FROM Classroom ORDER BY building, room_number")
    rows = cur.fetchall()
    conn.close()
    return rows


def get_all_timeslots():
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("""
        SELECT timeslot_ID, weekday, start_time, end_time
        FROM Timeslot
        ORDER BY weekday, start_time
    """)
    rows = cur.fetchall()
    conn.close()
    return rows
