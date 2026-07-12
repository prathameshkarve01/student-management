from database import SessionLocal
from models import User, Student

db = SessionLocal()

# Add students
amit = Student(
    name="Amit",
    course="Python"
)

john = Student(
    name="John",
    course="AWS"
)

db.add(amit)
db.add(john)
db.commit()

db.refresh(amit)
db.refresh(john)


# Add login users

amit_user = User(
    username="amit",
    password="amit123",
    role="student",
    student_id=amit.id
)

john_user = User(
    username="john",
    password="john123",
    role="student",
    student_id=john.id
)

db.add(amit_user)
db.add(john_user)

db.commit()

db.close()

print("Students created")