from datetime import date, time, timedelta
from pydantic import BaseModel



# Pydantic model for incoming data
class AttendanceCreate(BaseModel):
    date: date
    time_in: time
    time_out: time
    break_hours: time
    working_hours: time
