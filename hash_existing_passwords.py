import bcrypt

from database import SessionLocal
from models import User

db = SessionLocal()

users = db.query(User).all()

for user in users:

    # Skip users whose password is already hashed
    if user.password.startswith("$2b$"):
        continue

    hashed_password = bcrypt.hashpw(
        user.password.encode(),
        bcrypt.gensalt()
    ).decode()

    user.password = hashed_password

db.commit()
db.close()

print("All existing passwords have been hashed successfully.")