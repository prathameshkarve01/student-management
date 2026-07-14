from fastapi.testclient import TestClient
import main
from database import SessionLocal
from models import User, Base
import bcrypt

Base.metadata.drop_all(bind=main.engine)
Base.metadata.create_all(bind=main.engine)

db = SessionLocal()
db.add(User(username='admin', password=bcrypt.hashpw(b'admin123', bcrypt.gensalt()).decode(), role='admin'))
db.commit()
db.close()

client = TestClient(main.app)
login_resp = client.post('/login', data={'username': 'admin', 'password': 'admin123'})
print('login_status', login_resp.status_code)
print('login_location', login_resp.headers.get('location'))

resp = client.post(
    '/students',
    data={'name': 'John', 'course': 'CS', 'username': 'john', 'password': '123', 'role': 'student'},
    follow_redirects=False,
)
print('add_status', resp.status_code)
print('add_location', resp.headers.get('location'))
print(resp.text)
