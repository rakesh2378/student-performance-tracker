# student-performance-tracker
A Python + Flask web application that helps teachers track student performance across different subjects. It supports both a menu-driven CLI and a web-based UI, with persistent data storage using SQLite (via SQLAlchemy).Includes:
- Core OOP classes (`Student`, `StudentTracker`) with SQLite persistence (SQLAlchemy).
- CLI menu tool for quick local use.
- Flask web UI with pages to add students, assign grades, view details, and generate class reports.
- Ready-to-deploy files for Heroku or any Gunicorn-compatible host.

## 1) Quick Start (Local)

```bash
python -m venv .venv
# Windows: .venv\Scripts\activate
# macOS/Linux:
source .venv/bin/activate

pip install -r requirements.txt

# Initialize and run the web app
python app.py
# Open http://127.0.0.1:5000/
```

Or use the CLI:
```bash
python cli.py
```

The SQLite database file `students.db` will be created automatically in the project folder.

## 2) Core Features
- **Add Students**: name + unique roll number.
- **Add Grades**: per subject (0–100); updates if subject exists.
- **View Student Details**: grades table + average.
- **Calculate Average**: per student.
- **Bonus Reports**:
  - Subject-wise topper.
  - Class average.
  - Save backup to a text file (`students_backup.txt`).

## 3) Code Structure
```
student_performance_tracker/
├─ app.py                 # Flask routes & views
├─ tracker.py             # OOP classes + SQLAlchemy models
├─ cli.py                 # Menu-driven console interface
├─ templates/
│  ├─ base.html
│  ├─ index.html
│  ├─ add_student.html
│  ├─ add_grade.html
│  ├─ student_detail.html
│  └─ class_reports.html
├─ static/                # (placeholder for assets)
├─ requirements.txt
├─ Procfile
└─ README_user_guide.md
```

## 4) API (Minimal Examples)

> The web app is designed for browser use, but you can extend `app.py` with JSON routes.  
> Below are examples you *can* add if you want API endpoints:

```python
# Example (add to app.py):
from flask import jsonify

@app.post("/api/students")
def api_add_student():
    data = request.json or {}
    ok = tracker.add_student(data.get("name",""), data.get("roll_number",""))
    return jsonify({"success": ok}), (201 if ok else 400)
```

## 5) Deployment (Heroku)

1. Create a new Git repository and push:
   ```bash
   git init
   git add .
   git commit -m "Student Performance Tracker"
   heroku create  # or create app on dashboard
   git push heroku main  # or: git push heroku HEAD:main
   ```
2. Ensure the following files exist:
   - `requirements.txt` – dependencies
   - `Procfile` – tells Heroku to run `gunicorn app:app`
3. (Optional) Set a secret key:
   ```bash
   heroku config:set SECRET_KEY=$(python -c "import secrets; print(secrets.token_hex(16))")
   ```
4. Open the app:
   ```bash
   heroku open
   ```

> Other hosts: Render, Railway, Fly.io, etc., also support Python + Gunicorn deployments similarly.

## 6) Usage Examples

### Add Students (Web)
- Go to **Add Student**.
- Enter *Name* and *Roll Number*.
- Submit; you’ll return to the list.

### Assign Grades (Web)
- From **Students** list, click **View** for a student.
- Click **Add Grade**.
- Enter *Subject* (e.g., Math) and *Score (0–100)*.
- Save; repeat for more subjects.

### Reports (Web)
- Click **Reports**.
- Enter a subject (e.g., *Math*).
- See class average and topper (if any).

### CLI Example
```
==== Student Performance Tracker (CLI) ====
1. Add student
2. Add/Update grades
3. View student details
...
```

## 7) Notes
- Grades are validated (0–100). Invalid entries are rejected.
- Roll numbers are globally unique.
- Updating a grade for an existing subject overwrites the previous score.

Enjoy!
