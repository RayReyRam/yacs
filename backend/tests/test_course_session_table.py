import datetime
import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import IntegrityError

from backend.tables.database import Base
from backend.tables.course_session import CourseSession

@pytest.fixture(scope="module")
def engine():
    # Use in-memory SQLite for fast, side-effect free tests
    engine = create_engine("sqlite:///:memory:")
    Base.metadata.create_all(engine)
    return engine

@pytest.fixture()
def db_session(engine):
    Session = sessionmaker(bind=engine)
    return Session()

def test_course_session_insert_and_query(db_session):
    cs = CourseSession(
        crn="12345",
        section="A",
        semester="Fall2025",
        time_start=datetime.time(9, 0),
        time_end=datetime.time(10, 0),
        day_of_week=1,
        location="Room 101",
        session_type="Lecture",
        instructor="Prof X",
    )
    db_session.add(cs)
    db_session.commit()

    fetched = db_session.query(CourseSession).filter_by(
        crn="12345", section="A", semester="Fall2025", day_of_week=1
    ).one()

    assert fetched.location == "Room 101"
    assert fetched.session_type == "Lecture"


def test_course_session_update(db_session):
    cs = CourseSession(
        crn="67890",
        section="B",
        semester="Fall2025",
        time_start=datetime.time(11, 0),
        time_end=datetime.time(12, 0),
        day_of_week=2,
        location="Room 202",
        session_type="Lab",
        instructor="Prof Y",
    )
    db_session.add(cs)
    db_session.commit()

    # Update
    cs.location = "Room 303"
    db_session.commit()
    refreshed = db_session.query(CourseSession).filter_by(
        crn="67890", section="B", semester="Fall2025", day_of_week=2
    ).one()
    assert refreshed.location == "Room 303"


def test_course_session_composite_pk_uniqueness(db_session):
    cs1 = CourseSession(
        crn="99999",
        section="C",
        semester="Fall2025",
        time_start=datetime.time(13, 0),
        time_end=datetime.time(14, 0),
        day_of_week=3,
        location="Room 404",
        session_type="Seminar",
        instructor="Prof Z",
    )
    db_session.add(cs1)
    db_session.commit()

    cs2 = CourseSession(
        crn="99999",  # same composite PK fields
        section="C",
        semester="Fall2025",
        time_start=datetime.time(15, 0),
        time_end=datetime.time(16, 0),
        day_of_week=3,
        location="Room 505",
        session_type="Seminar",
        instructor="Prof Z",
    )
    db_session.add(cs2)
    with pytest.raises(IntegrityError):
        db_session.commit()
    db_session.rollback()
