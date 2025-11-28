from flask import Blueprint, render_template, request, redirect
from models import *

student_bp = Blueprint("student", __name__, url_prefix="/student")

@student_bp.route("/dashboard")
def dashboard():
    student_id = 1  # TODO: replace with session
    return render_template("student/dashboard.html")

