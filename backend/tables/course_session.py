from sqlalchemy import Column, PrimaryKeyConstraint
from sqlalchemy.dialects.postgresql import INTEGER, VARCHAR, TIME

from .database import Base

class CourseSession(Base):
    __tablename__ = "course_session"

    crn = Column(VARCHAR(length=255))
    section = Column(VARCHAR(length=255))
    semester = Column(VARCHAR(length=255))
    time_start = Column(TIME)
    time_end = Column(TIME)
    day_of_week = Column(INTEGER)
    location = Column(VARCHAR(length=255))
    session_type = Column(VARCHAR(length=255))
    instructor = Column(VARCHAR(length=255))

    __table_args__ = (
        PrimaryKeyConstraint('crn', 'section', 'semester', 'day_of_week'),
    )

    def conflicts_with(self, other_session):
        """Check if this session conflicts with another session on the same day."""
        if self.day_of_week != other_session.day_of_week:
            return False
        
        return not (self.time_end <= other_session.time_start or 
                   self.time_start >= other_session.time_end)

    def get_duration_minutes(self):
        """Calculate session duration in minutes."""
        from datetime import datetime
        start = datetime.combine(datetime.today(), self.time_start)
        end = datetime.combine(datetime.today(), self.time_end)
        return int((end - start).total_seconds() / 60)
