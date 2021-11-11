from flask import Flask
from models import User, Event, Session

app = Flask(__name__)

user1 = User(id=1, username="Vasyl Kovalchuk", firstName="Vasyl", lastName="Kovalchuk", email="vaskov@gmail.com", password="123", phone="093000")
event1 = Event(id=1, name='Birthday', owner_id=1)

user2 = User(id=2, username="Ivan M", firstName="Ivan", lastName="M", email="Iv@gmail.com", password="1000", phone="0978563")
event2 = Event(id=2, name='Wedding', owner_id=2)

user3 = User(id=3, username="Petro B", firstName="Petro", lastName="B", email="petr@gmail.com", password="1111", phone="0994123")
event3 = Event(id=3, name='Birthday', owner_id=3)

with Session() as session:
    session.add(user1)
    session.commit()
    session.add(event1)
    session.commit()

    session.add(user2)
    session.commit()
    session.add(event2)
    session.commit()

    session.add(user3)
    session.commit()
    session.add(event3)
    session.commit()
print(session.query(User).all())