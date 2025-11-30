from flask import Flask, render_template
from routes.admin import admin_bp
from routes.instructor import instructor_bp
from routes.student import student_bp
from routes.auth import auth_bp

app = Flask(__name__)
app.secret_key = "YOUR_SECRET_KEY_HERE"

# Register blueprints
app.register_blueprint(auth_bp)
app.register_blueprint(student_bp, url_prefix="/student")
app.register_blueprint(instructor_bp, url_prefix="/instructor")
app.register_blueprint(admin_bp, url_prefix="/admin")

@app.route("/")
def index():
    return render_template("index.html")

if __name__ == "__main__":
    app.run(debug=True)
