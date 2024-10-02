from datetime import date, time, timedelta
from pydantic import BaseModel

# Pydantic model for incoming data
class AttendanceCreate(BaseModel):
    user_id: int
    date: date
    time_in: time
    time_out: time
    break_hours: timedelta
    working_hours: timedelta
