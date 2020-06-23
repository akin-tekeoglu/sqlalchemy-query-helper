import datetime
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import pytest
from sqlalchemy_query_generator.query_generator import QueryGenerator
from tests.model import Base, User

engine = create_engine("sqlite:///:memory:", echo=True)
Session = sessionmaker(bind=engine)


@pytest.fixture(scope="function", name="session_fixture")
def _session_fixture():
    Base.metadata.create_all(engine)
    session = Session()
    yield session
    session.close()
    Base.metadata.drop_all(bind=engine)


generator = QueryGenerator()


def test_eq_operator(session_fixture):
    ed_user1 = User(name="ed", fullname="Ed Jones", nickname="edsnickname")
    ed_user2 = User(name="eds", fullname="Ed Jones", nickname="edsnickname")
    session_fixture.add(ed_user1)
    session_fixture.add(ed_user2)
    query = generator.generate(
        session_fixture, User, {"name": {"op": "eq", "value": ed_user1.name}}
    )
    result = list(query)
    assert len(result) == 1
    assert result[0].name == ed_user1.name


def test_gte_with_datetime(session_fixture):
    ed_user1 = User(
        name="ed",
        fullname="Ed Jones",
        nickname="edsnickname",
        timestamp=datetime.datetime.utcnow() + datetime.timedelta(days=1),
    )
    ed_user2 = User(
        name="ed",
        fullname="Ed Jones",
        nickname="edsnickname",
        timestamp=datetime.datetime.utcnow() - datetime.timedelta(days=1),
    )
    session_fixture.add(ed_user1)
    session_fixture.add(ed_user2)
    query = generator.generate(
        session_fixture,
        User,
        {"timestamp": {"op": "gte", "value": ed_user1.timestamp}},
    )
    result = list(query)
    assert len(result) == 1
    assert result[0].timestamp >= ed_user1.timestamp
