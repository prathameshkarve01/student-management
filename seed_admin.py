from database import SessionLocal
from models import User
from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

db = SessionLocal()

admin = db.query(User).filter(User.username == "admin").first()

if not admin:
    user = User(
        username="admin",
        password=pwd_context.hash("admin123"),
        role="admin"
    )
    db.add(user)
    db.commit()
    print("Admin user created")
else:
    print("Admin already exists")

db.close()