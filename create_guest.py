import bcrypt

from database import SessionLocal
from models import User

db = SessionLocal()

hashed_password = bcrypt.hashpw(
    "guest123".encode(),
    bcrypt.gensalt()
).decode()

guest = User(
    username="guest",
    password=hashed_password,
    role="user",
    student_id=None
)

db.add(guest)
db.commit()

print("Guest user created!")

db.close()