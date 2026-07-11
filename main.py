from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session

from database import engine, SessionLocal
from models import Base, Student

app = FastAPI()

Base.metadata.create_all(bind=engine)


# Database connection
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.get("/")
def home():
    return {"message": "Student Management System Running"}


# Get all students
@app.get("/students")
def get_students(db: Session = Depends(get_db)):
    students = db.query(Student).all()
    return students


# Add student
@app.post("/students")
def add_student(student: dict, db: Session = Depends(get_db)):

    new_student = Student(
        name=student["name"],
        course=student["course"]
    )

    db.add(new_student)
    db.commit()
    db.refresh(new_student)

    return {
        "message": "Student added successfully",
        "student": new_student
    }