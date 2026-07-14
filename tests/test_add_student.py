import unittest

from fastapi.responses import JSONResponse

from database import SessionLocal, engine
from main import add_student
from models import Base, User


class FakeRequest:
    def __init__(self, role="admin"):
        self.session = {"role": role}


class AddStudentTests(unittest.TestCase):
    def setUp(self):
        Base.metadata.drop_all(bind=engine)
        Base.metadata.create_all(bind=engine)

    def test_duplicate_username_returns_user_friendly_error(self):
        db = SessionLocal()
        db.add(User(username="existing", password="hashed", role="student"))
        db.commit()
        db.close()

        response = add_student(
            request=FakeRequest(),
            name="John",
            course="CS",
            username="existing",
            password="123456",
            role="student",
            db=SessionLocal(),
        )

        self.assertIsInstance(response, JSONResponse)
        self.assertEqual(response.status_code, 400)
        self.assertIn("Username already exists", response.body.decode())


if __name__ == "__main__":
    unittest.main()
