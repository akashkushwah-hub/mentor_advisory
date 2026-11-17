from database import MentorModel, SessionLocal, StudentModel, init_db
from engine import aggregate_batch_analytics, assign_mentor_to_student, run_risk_assessment_engine
from flask import Flask, redirect, render_template, request, url_for
from sqlalchemy import or_
from sqlalchemy.orm import joinedload
app = Flask(__name__)


@app.route("/")
def dashboard():
    run_risk_assessment_engine()

    query = request.args.get("search", "").strip()
    db = SessionLocal()

    # Use joinedload to fetch assigned_mentor alongside student records
    base_query = db.query(StudentModel).options(joinedload(StudentModel.assigned_mentor))

    if query:
        students = base_query.filter(
            or_(
                StudentModel.student_id.ilike(f"%{query}%"),
                StudentModel.name.ilike(f"%{query}%"),
                StudentModel.risk_level.ilike(f"%{query}%"),
            )
        ).all()
    else:
        students = base_query.all()

    mentors = db.query(MentorModel).all()
    analytics = aggregate_batch_analytics("B2026-CS")

    # Keep session open or close safely after eager loading
    db.close()

    return render_template(
        "dashboard.html",
        students=students,
        mentors=mentors,
        analytics=analytics,
        search_query=query,
    )


@app.route("/allocate/<student_id>")
def allocate(student_id):
    assign_mentor_to_student(student_id)
    return redirect(url_for("dashboard", search=request.args.get("search", "")))


if __name__ == "__main__":
    init_db()
    app.run(debug=True, port=5000)