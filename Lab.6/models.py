from sqlalchemy import create_engine, Column, Integer, String, ForeignKey, Table
from sqlalchemy.orm import sessionmaker, scoped_session, declarative_base


engine = create_engine(f"mysql+mysqlconnector://root:root@localhost:3307/pp1")
connect = engine.connect()

SessionFactory = sessionmaker(bind=engine)
Session = scoped_session(SessionFactory)
Base = declarative_base()


class User(Base):
    __tablename__ = "User"

    id = Column(Integer(), primary_key=True, autoincrement=True)
    username = Column(String(100), nullable=False)
    firstName = Column(String(100), nullable=False)
    lastName = Column(String(100), nullable=False)
    email = Column(String(100), nullable=False)
    password = Column(String(100), nullable=False)
    phone = Column(Integer(), nullable=False)


class Event(Base):
    __tablename__ = "Event"

    id = Column(Integer(), primary_key=True, autoincrement=True)
    name = Column(String(100), nullable=False)
    owner_id = Column(Integer(), ForeignKey('User.id'))


# user_event = Table('User_Event', Base.metadata,
#                    Column('id', Integer(), primary_key=True),
#                    Column('user_id', ForeignKey("User.id")),
#                    Column('event_id', ForeignKey("Event.id"))
#                    )

class user_event(Base):
    __tablename__ = "User_Event"
    id = Column(Integer(), primary_key=True)
    user_id = Column(Integer(), ForeignKey("User.id"))
    event_id = Column(Integer(), ForeignKey("Event.id"))