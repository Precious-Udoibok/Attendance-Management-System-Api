#attendance report models
from sqlalchemy import Column, Integer, String, Date, ForeignKey, Boolean
from ..database import database
from sqlalchemy import create_engine, Column, Integer, String, Date, Time, Interval, TIMESTAMP

# User Model
class ATMS_REPORT(database.Base):
    __tablename__ = "AMS_users_report"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, nullable=False)
    date = Column(Date, nullable=False)
    time_in = Column(Time, nullable=False)
    time_out = Column(Time, nullable=False)
    break_hours = Column(Interval, nullable=False)
    working_hours = Column(Interval, nullable=False)
    # created_at = Column(TIMESTAMP, default="now()")

    
