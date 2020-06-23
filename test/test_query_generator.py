from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy import inspect
from sqlalchemy_query_generator.query_generator import QueryGenerator

engine = create_engine("sqlite:///:memory:", echo=True)

Base = declarative_base()


class User(Base):
    __tablename__ = "user"
    id = Column(Integer, primary_key=True)
    name = Column(String)
    fullname = Column(String)
    nickname = Column(String)


# inst = inspect(User)
Base.metadata.create_all(engine)
Session = sessionmaker()
Session.configure(bind=engine)

generator = QueryGenerator()


def test_equality_operator():
    session = Session()
    ed_user = User(name="ed", fullname="Ed Jones", nickname="edsnickname")
    session.add(ed_user)
    query = generator.generate(
        session, User, {"name": {"op": "eq", "value": ed_user.name}}
    )
    result = list(query)
    assert len(result) == 1
    assert result[0].name == ed_user.name
