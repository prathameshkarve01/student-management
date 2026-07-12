from fastapi import FastAPI, Depends, Request, Form
from sqlalchemy.orm import Session

from database import engine, SessionLocal
from models import Base, Student

from fastapi import Request
from fastapi.templating import Jinja2Templates

#Importing the Schemas.py file to use the Pydantic models for request validation
from schemas import StudentCreate

from fastapi import Query
#Importing RedirectResponse to redirect the user to a different page after a successful operation
from fastapi.responses import RedirectResponse

app = FastAPI()
#for templates
templates = Jinja2Templates(directory="templates")

Base.metadata.create_all(bind=engine)


# Database connection
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.get("/")
def home(request: Request):
    return templates.TemplateResponse(
        request=request,
        name="index.html",
        context={"request": request}
    )
# Dashboard route with query parameter
@app.get("/dashboard")
def dashboard(
    request: Request,
    role: str = Query(...),
    db: Session = Depends(get_db)
):

    students = db.query(Student).all()

    return templates.TemplateResponse(
        request=request,
        name="dashboard.html",
        context={
            "request": request,
            "role": role,
            "students": students
        }
    )

# Get all students
@app.get("/students")
def get_students(db: Session = Depends(get_db)):
    students = db.query(Student).all()
    return students


# Add student
@app.post("/students")
def add_student(
    name: str = Form(...),
    course: str = Form(...),
    db: Session = Depends(get_db)
):

    new_student = Student(
        name=name,
        course=course
    )

    db.add(new_student)
    db.commit()
    db.refresh(new_student)

    return RedirectResponse(
    url="/dashboard?role=admin",
    status_code=303
)

# Delete student
@app.get("/delete/{student_id}")
def delete_student(
    student_id: int,
    db: Session = Depends(get_db)
):

    student = db.query(Student).filter(Student.id == student_id).first()

    if student:
        db.delete(student)
        db.commit()

    return RedirectResponse(
        url="/dashboard?role=admin",
        status_code=303
    )

# Edit student
@app.get("/edit/{student_id}")
def edit_student(
    student_id: int,
    request: Request,
    db: Session = Depends(get_db)
):

    student = db.query(Student).filter(Student.id == student_id).first()

    return templates.TemplateResponse(
        request=request,
        name="edit.html",
        context={
            "request": request,
            "student": student
        }
    )
@app.post("/update/{student_id}")
def update_student(
    student_id: int,
    name: str = Form(...),
    course: str = Form(...),
    db: Session = Depends(get_db)
):

    student = db.query(Student).filter(Student.id == student_id).first()

    if student:
        student.name = name
        student.course = course

        db.commit()

    return RedirectResponse(
        url="/dashboard?role=admin",
        status_code=303
    )