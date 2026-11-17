from datetime import datetime
from sqlalchemy import Column, DateTime, Float, ForeignKey, Integer, String, create_engine
from sqlalchemy.orm import declarative_base, relationship, sessionmaker

DATABASE_URL = "sqlite:///academic_advisory.db"

engine = create_engine(DATABASE_URL, echo=False)
SessionLocal = sessionmaker(bind=engine)
Base = declarative_base()


# ==========================================
# ORM MODELS
# ==========================================
class MentorModel(Base):
    __tablename__ = "mentors"

    mentor_id = Column(String, primary_key=True)
    name = Column(String, nullable=False)
    specialization = Column(String, nullable=False)
    current_students = Column(Integer, default=0)
    max_capacity = Column(Integer, default=10)

    students = relationship("StudentModel", back_populates="assigned_mentor")


class StudentModel(Base):
    __tablename__ = "students"

    student_id = Column(String, primary_key=True)
    name = Column(String, nullable=False)
    batch_id = Column(String, nullable=False)
    attendance_pct = Column(Float, nullable=False)
    avg_score_pct = Column(Float, nullable=False)
    pending_assignments = Column(Integer, default=0)
    failed_subjects = Column(Integer, default=0)
    weak_subject = Column(String, nullable=False)
    risk_index = Column(Float, default=0.0)
    risk_level = Column(String, default="NONE")

    assigned_mentor_id = Column(String, ForeignKey("mentors.mentor_id"), nullable=True)
    assigned_mentor = relationship("MentorModel", back_populates="students")


class SubjectScoreModel(Base):
    __tablename__ = "subject_scores"

    id = Column(Integer, primary_key=True, autoincrement=True)
    batch_id = Column(String, nullable=False)
    subject_name = Column(String, nullable=False)
    avg_score = Column(Float, nullable=False)


# ==========================================
# DATABASE SEEDING (6 PROFESSORS & 30 STUDENTS)
# ==========================================
def init_db():
    Base.metadata.create_all(engine)
    db = SessionLocal()

    if not db.query(MentorModel).first():
        mentors = [
            MentorModel(mentor_id="M101", name="Dr. Alan Turing", specialization="Mathematics", max_capacity=10),
            MentorModel(mentor_id="M102", name="Prof. Ada Lovelace", specialization="Computer Science", max_capacity=10),
            MentorModel(mentor_id="M103", name="Dr. Grace Hopper", specialization="Data Science", max_capacity=10),
            MentorModel(mentor_id="M104", name="Dr. Richard Feynman", specialization="Physics", max_capacity=10),
            MentorModel(mentor_id="M105", name="Prof. Claude Shannon", specialization="Information Theory", max_capacity=10),
            MentorModel(mentor_id="M106", name="Dr. Katherine Johnson", specialization="Applied Mathematics", max_capacity=10),
        ]

        raw_students = [
            ("S101", "John Doe", "B2026-CS", 48.0, 35.0, 4, 2, "Computer Science"),
            ("S102", "Jane Smith", "B2026-CS", 82.0, 78.0, 0, 0, "Mathematics"),
            ("S103", "Alex Brown", "B2026-CS", 62.0, 45.0, 2, 1, "Data Science"),
            ("S104", "Emily Davis", "B2026-CS", 91.0, 88.0, 0, 0, "Physics"),
            ("S105", "Michael Wilson", "B2026-CS", 42.0, 31.0, 5, 3, "Mathematics"),
            ("S106", "Sarah Miller", "B2026-CS", 75.0, 65.0, 1, 0, "Information Theory"),
            ("S107", "David Taylor", "B2026-CS", 58.0, 48.0, 3, 1, "Computer Science"),
            ("S108", "Jessica Anderson", "B2026-CS", 88.0, 82.0, 0, 0, "Data Science"),
            ("S109", "James Thomas", "B2026-CS", 39.0, 28.0, 6, 2, "Physics"),
            ("S110", "Emma Jackson", "B2026-CS", 95.0, 92.0, 0, 0, "Mathematics"),
            ("S111", "Daniel White", "B2026-CS", 68.0, 52.0, 2, 0, "Applied Mathematics"),
            ("S112", "Sophia Harris", "B2026-CS", 52.0, 41.0, 4, 1, "Information Theory"),
            ("S113", "Matthew Martin", "B2026-CS", 84.0, 74.0, 0, 0, "Computer Science"),
            ("S114", "Olivia Thompson", "B2026-CS", 46.0, 38.0, 3, 2, "Data Science"),
            ("S115", "Ethan Garcia", "B2026-CS", 78.0, 69.0, 1, 0, "Physics"),
            ("S116", "Isabella Martinez", "B2026-CS", 90.0, 85.0, 0, 0, "Mathematics"),
            ("S117", "Alexander Robinson", "B2026-CS", 35.0, 25.0, 5, 3, "Applied Mathematics"),
            ("S118", "Mia Clark", "B2026-CS", 72.0, 60.0, 2, 0, "Computer Science"),
            ("S119", "William Rodriguez", "B2026-CS", 61.0, 49.0, 3, 1, "Physics"),
            ("S120", "Charlotte Lewis", "B2026-CS", 86.0, 80.0, 0, 0, "Data Science"),
            ("S121", "Benjamin Lee", "B2026-CS", 49.0, 37.0, 4, 2, "Information Theory"),
            ("S122", "Amelia Walker", "B2026-CS", 93.0, 89.0, 0, 0, "Mathematics"),
            ("S123", "Lucas Hall", "B2026-CS", 55.0, 44.0, 3, 1, "Applied Mathematics"),
            ("S124", "Harper Allen", "B2026-CS", 80.0, 71.0, 1, 0, "Computer Science"),
            ("S125", "Henry Young", "B2026-CS", 40.0, 30.0, 5, 2, "Physics"),
            ("S126", "Evelyn Hernandez", "B2026-CS", 87.0, 79.0, 0, 0, "Data Science"),
            ("S127", "Jacob King", "B2026-CS", 64.0, 53.0, 2, 0, "Information Theory"),
            ("S128", "Abigail Wright", "B2026-CS", 51.0, 42.0, 4, 1, "Mathematics"),
            ("S129", "Logan Scott", "B2026-CS", 89.0, 84.0, 0, 0, "Applied Mathematics"),
            ("S130", "Ella Green", "B2026-CS", 44.0, 33.0, 4, 2, "Computer Science"),
        ]

        students = [
            StudentModel(
                student_id=s[0],
                name=s[1],
                batch_id=s[2],
                attendance_pct=s[3],
                avg_score_pct=s[4],
                pending_assignments=s[5],
                failed_subjects=s[6],
                weak_subject=s[7],
            )
            for s in raw_students
        ]

        scores = [
            SubjectScoreModel(batch_id="B2026-CS", subject_name="Computer Science", avg_score=58.0),
            SubjectScoreModel(batch_id="B2026-CS", subject_name="Mathematics", avg_score=52.0),
            SubjectScoreModel(batch_id="B2026-CS", subject_name="Data Science", avg_score=64.0),
            SubjectScoreModel(batch_id="B2026-CS", subject_name="Physics", avg_score=48.0),
            SubjectScoreModel(batch_id="B2026-CS", subject_name="Applied Mathematics", avg_score=50.0),
        ]

        db.add_all(mentors)
        db.add_all(students)
        db.add_all(scores)
        db.commit()

    db.close()