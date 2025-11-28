from flask import Flask, render_template
from routes.admin import admin_bp
from routes.instructor import instructor_bp
#from routes.student import student_bp

app = Flask(__name__)

# Register blueprints
app.register_blueprint(admin_bp)
app.register_blueprint(instructor_bp)
#app.register_blueprint(student_bp)

@app.route("/")
def index():
    return render_template("index.html")

if __name__ == "__main__":
    app.run(debug=True)
