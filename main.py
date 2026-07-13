from fastapi import FastAPI, Depends, Request, Form
from sqlalchemy.orm import Session

from database import engine, SessionLocal
from models import Base, Student, User

from fastapi import Request
from fastapi.templating import Jinja2Templates



from fastapi import Query
#Importing RedirectResponse to redirect the user to a different page after a successful operation
from fastapi.responses import RedirectResponse


from starlette.middleware.sessions import SessionMiddleware

import bcrypt

app = FastAPI()

app.add_middleware(
    SessionMiddleware,
    secret_key="mysecretkey"
)
#for templates
templates = Jinja2Templates(directory="templates")
import os

print("Database path:", os.path.abspath("students.db"))
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

#Login route to authenticate the user and redirect to the dashboard with the role as a query parameter
@app.post("/login")
def login(
    request: Request,
    username: str = Form(...),
    password: str = Form(...),
    db: Session = Depends(get_db)
):

    # Find user only by username
    user = db.query(User).filter(
        User.username == username
    ).first()
    print("Username entered:", username)

    if user:
        print("Password in DB:", user.password)

    # Check if user exists
    if not user:
        return {"message": "Invalid Username or Password"}
    print("Password entered:", password)
    # Verify hashed password
    if not bcrypt.checkpw(
        password.encode(),
        user.password.encode()
    ):
        return {"message": "Invalid Username or Password"}

    # Store login details in session
    request.session["user_id"] = user.id
    request.session["role"] = user.role

    return RedirectResponse(
        url="/dashboard",
        status_code=303
    )

# Dashboard route with query parameter
@app.get("/dashboard")
def dashboard(
    request: Request,
    db: Session = Depends(get_db)
):

    role = request.session.get("role")

    if not role:
        return RedirectResponse(
            url="/",
            status_code=303
        )

    user_student_id = None
    student_name = None

    if role == "student":

        user_id = request.session.get("user_id")

        user = db.query(User).filter(
            User.id == user_id
        ).first()

        user_student_id = user.student_id

        student = db.query(Student).filter(
            Student.id == user.student_id
        ).first()

        student_name = student.name


    students = db.query(Student).all()

    return templates.TemplateResponse(
        request=request,
        name="dashboard.html",
        context={
            "request": request,
            "role": role,
            "students": students,
            "user_student_id": user_student_id,
            "student_name": student_name
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
    request: Request,
    name: str = Form(...),
    course: str = Form(...),
    username: str = Form(...),
    password: str = Form(...),
    role: str = Form(...),
    db: Session = Depends(get_db)
):

    logged_in_role = request.session.get("role")


    if logged_in_role != "admin":
        return {"message": "Access Denied"}

    student_id = None

    if role == "student":

        new_student = Student(
            name=name,
            course=course
            )

        db.add(new_student)
        db.commit()
        db.refresh(new_student)

        student_id = new_student.id

    #create login account for the student
    hashed_password = bcrypt.hashpw(
        password.encode(),
        bcrypt.gensalt()
    ).decode()

    new_user = User(
        username=username,
        password=hashed_password,
        role=role,
        student_id=student_id
    )

    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return RedirectResponse(
        url="/dashboard",
        status_code=303
    )

# Delete student
@app.get("/delete/{student_id}")
def delete_student(
    student_id: int,
    request: Request,
    db: Session = Depends(get_db)
):

    role = request.session.get("role")

    if role != "admin":
        return {"message": "Access Denied"}

    student = db.query(Student).filter(
        Student.id == student_id
    ).first()

    if student:
        db.delete(student)
        db.commit()

    return RedirectResponse(
        url="/dashboard",
        status_code=303
    )

# Edit student
@app.get("/edit/{student_id}")
def edit_student(
    student_id: int,
    request: Request,
    db: Session = Depends(get_db)
):

    role = request.session.get("role")

    # Student can edit only their own record
    if role == "student":

        user_id = request.session.get("user_id")

        user = db.query(User).filter(
            User.id == user_id
        ).first()

        if student_id != user.student_id:
            return {"message": "Access Denied"}


    # Admin can edit anyone
    student = db.query(Student).filter(
        Student.id == student_id
    ).first()


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
    request: Request,
    name: str = Form(...),
    course: str = Form(...),
    db: Session = Depends(get_db)
):

    role = request.session.get("role")

    # Student can update only their own data
    if role == "student":

        user_id = request.session.get("user_id")

        user = db.query(User).filter(
            User.id == user_id
        ).first()

        if student_id != user.student_id:
            return {"message": "Access Denied"}


    # Admin and allowed student can update
    student = db.query(Student).filter(
        Student.id == student_id
    ).first()


    if student:
        student.name = name
        student.course = course

        db.commit()


    return RedirectResponse(
        url="/dashboard",
        status_code=303
    )

#Logout
@app.get("/logout")
def logout(request: Request):

    request.session.clear()

    return RedirectResponse(
        url="/",
        status_code=303
    )