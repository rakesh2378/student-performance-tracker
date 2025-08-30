"""
Student Performance Tracker - Core Logic (OOP + DB)
--------------------------------------------------
Implements Student and StudentTracker classes.
Backed by SQLite via SQLAlchemy ORM.
"""

from dataclasses import dataclass
from typing import Dict, Optional, List, Tuple
from statistics import mean
from sqlalchemy import create_engine, Column, Integer, String, Float, ForeignKey, UniqueConstraint
from sqlalchemy.orm import declarative_base, relationship, sessionmaker

# SQLAlchemy setup
Base = declarative_base()

class StudentModel(Base):
    __tablename__ = "students"
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    roll_number = Column(String, nullable=False, unique=True)
    grades = relationship("GradeModel", back_populates="student", cascade="all, delete-orphan")

class GradeModel(Base):
    __tablename__ = "grades"
    id = Column(Integer, primary_key=True)
    subject = Column(String, nullable=False)
    score = Column(Float, nullable=False)
    student_id = Column(Integer, ForeignKey("students.id"), nullable=False)
    student = relationship("StudentModel", back_populates="grades")
    __table_args__ = (UniqueConstraint("subject", "student_id", name="uq_subject_per_student"), )

# Public dataclass representation
@dataclass
class Student:
    name: str
    roll_number: str
    grades: Dict[str, float]

class StudentTracker:
    def __init__(self, db_url: str = "sqlite:///students.db"):
        self.engine = create_engine(db_url, echo=False, future=True)
        Base.metadata.create_all(self.engine)
        self.Session = sessionmaker(bind=self.engine, expire_on_commit=False)

    # Helper: validate grade range
    @staticmethod
    def _validate_grade(score: float) -> float:
        try:
            s = float(score)
        except (TypeError, ValueError):
            raise ValueError("Score must be a number")
        if s < 0 or s > 100:
            raise ValueError("Score must be between 0 and 100")
        return s

    def add_student(self, name: str, roll_number: str) -> bool:
        """Add a new student if roll_number is unique. Returns True if added."""
        with self.Session() as session:
            exists = session.query(StudentModel).filter_by(roll_number=roll_number).first()
            if exists:
                return False
            s = StudentModel(name=name.strip(), roll_number=roll_number.strip())
            session.add(s)
            session.commit()
            return True

    def add_grades(self, roll_number: str, grades: Dict[str, float]) -> Tuple[bool, str]:
        """Add or update grades for a student; returns (success, message)."""
        with self.Session() as session:
            student = session.query(StudentModel).filter_by(roll_number=roll_number).first()
            if not student:
                return False, "Student not found"
            for subject, score in grades.items():
                subject = subject.strip().title()
                s = self._validate_grade(score)
                g = next((g for g in student.grades if g.subject == subject), None)
                if g:
                    g.score = s  # update
                else:
                    student.grades.append(GradeModel(subject=subject, score=s))
            session.commit()
            return True, "Grades saved"

    def view_student_details(self, roll_number: str) -> Optional[Student]:
        with self.Session() as session:
            s = session.query(StudentModel).filter_by(roll_number=roll_number).first()
            if not s:
                return None
            grades = {g.subject: g.score for g in s.grades}
            return Student(name=s.name, roll_number=s.roll_number, grades=grades)

    def calculate_average(self, roll_number: str) -> Optional[float]:
        st = self.view_student_details(roll_number)
        if not st or not st.grades:
            return None
        return round(mean(st.grades.values()), 2)

    def subject_topper(self, subject: str) -> Optional[Tuple[str, str, float]]:
        """Return (name, roll_number, score) of top student in subject."""
        subject = subject.strip().title()
        with self.Session() as session:
            q = (session.query(StudentModel.name, StudentModel.roll_number, GradeModel.score)
                        .join(GradeModel, StudentModel.id == GradeModel.student_id)
                        .filter(GradeModel.subject == subject)
                        .order_by(GradeModel.score.desc()))
            top = q.first()
            return (top[0], top[1], top[2]) if top else None

    def class_average(self, subject: str) -> Optional[float]:
        subject = subject.strip().title()
        with self.Session() as session:
            scores = [g.score for g in session.query(GradeModel).filter_by(subject=subject).all()]
            return round(mean(scores), 2) if scores else None

    def list_students(self) -> List[Student]:
        with self.Session() as session:
            students = session.query(StudentModel).all()
            out = []
            for s in students:
                grades = {g.subject: g.score for g in s.grades}
                out.append(Student(name=s.name, roll_number=s.roll_number, grades=grades))
            return out

    def save_backup(self, filepath: str = "students_backup.txt") -> str:
        """Save all data to a local text file as a simple backup."""
        students = self.list_students()
        lines = []
        for st in students:
            grades_str = ", ".join(f"{sub}:{score}" for sub, score in st.grades.items()) or "No grades"
            avg = round(mean(st.grades.values()), 2) if st.grades else "N/A"
            lines.append(f"{st.roll_number}\t{st.name}\t{grades_str}\tAverage:{avg}")
        content = "\n".join(lines)
        with open(filepath, "w", encoding="utf-8") as f:
            f.write(content)
        return filepath
