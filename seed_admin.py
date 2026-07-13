from database import engine, SessionLocal
from models import Base, User
from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# Create tables if they don't exist
Base.metadata.create_all(bind=engine)

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
