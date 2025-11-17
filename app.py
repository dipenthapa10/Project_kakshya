from flask import Flask, render_template, request, redirect, url_for, session, flash
import pymysql
from werkzeug.security import check_password_hash
from config import get_connection

app = Flask(__name__)
app.secret_key = "change-this-secret-key"   # IMPORTANT: change this in real project


# --- HOME / LANDING PAGE --- #
@app.route("/")
def home():
    # If already logged in, send to dashboard based on role
    if "user_id" in session and "role" in session:
        role = session["role"]
        if role == "admin":
            return redirect(url_for("admin_dashboard"))
        elif role == "instructor":
            return redirect(url_for("instructor_dashboard"))
        elif role == "student":
            return redirect(url_for("student_dashboard"))
    return redirect(url_for("login"))

# --- LOGIN --- #
@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email_or_username = request.form.get("username")
        password = request.form.get("password")

        conn = get_connection()
        try:
            with conn.cursor() as cur:
                # 👇 Adjust this query to your actual User table & columns
                # Example User table: user_id, username, password_hash, role
                sql = """
                    SELECT user_id, username, password_hash, role
                    FROM User
                    WHERE username = %s
                """
                cur.execute(sql, (email_or_username,))
                user = cur.fetchone()
        finally:
            conn.close()

        if user and check_password_hash(user["password_hash"], password):
            # Save minimal info in session
            session["user_id"] = user["user_id"]
            session["username"] = user["username"]
            session["role"] = user["role"]

            # Redirect based on role
            if user["role"] == "admin":
                return redirect(url_for("admin_dashboard"))
            elif user["role"] == "instructor":
                return redirect(url_for("instructor_dashboard"))
            elif user["role"] == "student":
                return redirect(url_for("student_dashboard"))
        else:
            flash("Invalid username or password", "error")

    return render_template("login.html")

# --- LOGOUT --- #
@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("login"))

# --- DASHBOARDS (STUBS FOR NOW) --- #
@app.route("/admin")
def admin_dashboard():
    if session.get("role") != "admin":
        return redirect(url_for("login"))
    return render_template("admin_dashboard.html")

@app.route("/instructor")
def instructor_dashboard():
    if session.get("role") != "instructor":
        return redirect(url_for("login"))
    return render_template("instructor_dashboard.html")

@app.route("/student")
def student_dashboard():
    if session.get("role") != "student":
        return redirect(url_for("login"))
    return render_template("student_dashboard.html")

if __name__ == "__main__":
    app.run(debug=True)
