from database import MentorModel, SessionLocal, StudentModel, SubjectScoreModel


def run_risk_assessment_engine():
    db = SessionLocal()
    students = db.query(StudentModel).all()

    for student in students:
        a = student.attendance_pct
        s = student.avg_score_pct
        p = student.pending_assignments
        f = student.failed_subjects

        att_factor = 0.0 if a >= 75 else (75 - a) * 1.5
        perf_factor = 0.0 if s >= 50 else (50 - s) * 1.2
        pending_factor = min(p * 10.0, 30.0)
        backlog_factor = min(f * 15.0, 30.0)

        risk_index = round(att_factor + perf_factor + pending_factor + backlog_factor, 2)

        if risk_index >= 60 or a < 50 or f >= 3:
            risk_level = "CRITICAL"
        elif risk_index >= 40 or a < 65:
            risk_level = "HIGH"
        elif risk_index >= 20 or a < 75:
            risk_level = "MEDIUM"
        elif risk_index > 0:
            risk_level = "LOW"
        else:
            risk_level = "NONE"

        student.risk_index = risk_index
        student.risk_level = risk_level

    db.commit()
    db.close()


def assign_mentor_to_student(student_id: str):
    db = SessionLocal()
    student = db.query(StudentModel).filter_by(student_id=student_id).first()

    if not student:
        db.close()
        raise ValueError("Student not found")

    available_mentors = db.query(MentorModel).filter(MentorModel.current_students < MentorModel.max_capacity).all()

    if not available_mentors:
        available_mentors = db.query(MentorModel).order_by(MentorModel.current_students.asc()).all()

    scored_mentors = []
    for mentor in available_mentors:
        domain_match = 100.0 if mentor.specialization.lower() == student.weak_subject.lower() else 20.0
        workload_score = ((mentor.max_capacity - mentor.current_students) / mentor.max_capacity) * 100.0
        mps = (domain_match * 0.6) + (workload_score * 0.4)
        scored_mentors.append((mentor, mps))

    scored_mentors.sort(key=lambda x: x[1], reverse=True)
    best_mentor = scored_mentors[0][0]

    student.assigned_mentor_id = best_mentor.mentor_id
    best_mentor.current_students += 1

    db.commit()
    db.close()


def aggregate_batch_analytics(batch_id: str):
    db = SessionLocal()
    students = db.query(StudentModel).filter_by(batch_id=batch_id).all()

    if not students:
        db.close()
        return {}

    total = len(students)
    avg_att = sum(s.attendance_pct for s in students) / total
    avg_score = sum(s.avg_score_pct for s in students) / total
    high_risk_count = sum(1 for s in students if s.risk_level in ["HIGH", "CRITICAL"])

    weakest_subjects = (
        db.query(SubjectScoreModel).filter_by(batch_id=batch_id).order_by(SubjectScoreModel.avg_score.asc()).limit(2).all()
    )

    db.close()
    return {
        "batch_id": batch_id,
        "total_students": total,
        "avg_attendance": f"{avg_att:.1f}%",
        "avg_score": f"{avg_score:.1f}%",
        "at_risk_ratio": f"{(high_risk_count / total) * 100:.1f}%",
        "weakest_subjects": [f"{s.subject_name} ({s.avg_score}%)" for s in weakest_subjects],
    }