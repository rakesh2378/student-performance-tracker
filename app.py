"""
Flask Web App for Student Performance Tracker
Run locally:
    export FLASK_APP=app.py
    flask run
or:
    python app.py
"""
from flask import Flask, render_template, request, redirect, url_for, flash
from tracker import StudentTracker
import os

app = Flask(__name__)
app.secret_key = os.environ.get("SECRET_KEY", "dev-secret")
tracker = StudentTracker(os.environ.get("DATABASE_URL", "sqlite:///students.db"))

@app.route("/")
def index():
    students = tracker.list_students()
    return render_template("index.html", students=students)

@app.route("/students/new", methods=["GET", "POST"])
def add_student():
    if request.method == "POST":
        name = request.form.get("name", "").strip()
        roll = request.form.get("roll_number", "").strip()
        if not name or not roll:
            flash("Name and roll number are required.", "error")
        else:
            ok = tracker.add_student(name, roll)
            if ok:
                flash("Student added.", "success")
                return redirect(url_for("index"))
            else:
                flash("Roll number already exists.", "error")
    return render_template("add_student.html")

@app.route("/students/<roll_number>")
def student_detail(roll_number):
    st = tracker.view_student_details(roll_number)
    if not st:
        flash("Student not found.", "error")
        return redirect(url_for("index"))
    avg = tracker.calculate_average(roll_number)
    return render_template("student_detail.html", student=st, avg=avg)

@app.route("/grades/<roll_number>/add", methods=["GET", "POST"])
def add_grade(roll_number):
    st = tracker.view_student_details(roll_number)
    if not st:
        flash("Student not found.", "error")
        return redirect(url_for("index"))
    if request.method == "POST":
        subject = request.form.get("subject", "").strip()
        score = request.form.get("score", "").strip()
        try:
            ok, msg = tracker.add_grades(roll_number, {subject: float(score)})
            flash(msg, "success" if ok else "error")
            return redirect(url_for("student_detail", roll_number=roll_number))
        except ValueError as e:
            flash(str(e), "error")
    return render_template("add_grade.html", student=st)

@app.route("/reports")
def reports():
    subject = request.args.get("subject", "").strip()
    topper = avg = None
    if subject:
        topper = tracker.subject_topper(subject)
        avg = tracker.class_average(subject)
    return render_template("class_reports.html", subject=subject, topper=topper, avg=avg)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)), debug=True)
