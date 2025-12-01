from flask import Blueprint, render_template, request, redirect, session
from werkzeug.security import generate_password_hash, check_password_hash
from models import get_connection
import pymysql

auth_bp = Blueprint("auth", __name__, url_prefix="/auth")


# ------------------------------
# SIGNUP
# ------------------------------
@auth_bp.route("/signup", methods=["GET", "POST"])
def signup():
    if request.method == "POST":
        name = request.form["name"]
        email = request.form["email"]
        username = request.form["username"]
        password = request.form["password"]
        role = request.form["role"]

        conn = get_connection()
        cur = conn.cursor()

        # check duplicate username
        cur.execute("SELECT * FROM User WHERE username=%s", (username,))
        if cur.fetchone():
            conn.close()
            return render_template("auth/signup.html", error="Username already exists")

        # split name
        parts = name.split()
        first = parts[0]
        last = parts[-1]
        middle = " ".join(parts[1:-1]) if len(parts) > 2 else None

        # insert into role table
        student_id = None
        instructor_id = None
        admin_id = None

        if role == "student":
            cur.execute("""
                INSERT INTO Student(first_name, middle_name, last_name, email)
                VALUES (%s, %s, %s, %s)
            """, (first, middle, last, email))
            student_id = cur.lastrowid

        elif role == "instructor":
            cur.execute("""
                INSERT INTO Instructor(first_name, middle_name, last_name, email)
                VALUES (%s, %s, %s, %s)
            """, (first, middle, last, email))
            instructor_id = cur.lastrowid

        elif role == "admin":
            cur.execute("""
                INSERT INTO Admin(first_name, last_name, email)
                VALUES (%s, %s, %s)
            """, (first, last, email))
            admin_id = cur.lastrowid

        # insert into User table
        cur.execute("""
            INSERT INTO User(username, password_hash, role, student_ID, instructor_ID, admin_ID)
            VALUES (%s, %s, %s, %s, %s, %s)
        """, (
            username,
            generate_password_hash(password),
            role,
            student_id,
            instructor_id,
            admin_id
        ))

        conn.commit()
        conn.close()

        return redirect("/auth/login")

    return render_template("auth/signup.html")



# ------------------------------
# LOGIN
# ------------------------------
@auth_bp.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        conn = get_connection()
        cur = conn.cursor(pymysql.cursors.DictCursor)

        cur.execute("SELECT * FROM User WHERE username=%s", (username,))
        user = cur.fetchone()
        conn.close()

        if not user or not check_password_hash(user["password_hash"], password):
            return render_template("auth/login.html", error="Invalid username or password")

        # store session
        session.clear()
        session["user_id"] = user["user_id"]
        session["role"] = user["role"]
        session["student_id"] = user["student_ID"]
        session["instructor_id"] = user["instructor_ID"]
        session["admin_id"] = user["admin_ID"]

        # redirect to dashboards
        if user["role"] == "admin":
            return redirect("/admin/dashboard")

        elif user["role"] == "instructor":
            return redirect("/instructor/dashboard")

        else:
            return redirect("/student/dashboard")

    return render_template("auth/login.html")


# ------------------------------
# LOGOUT
# ------------------------------
@auth_bp.route("/logout")
def logout():
    session.clear()
    return redirect("/")

