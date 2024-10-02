#store the users attendance report
from fastapi import APIRouter,Depends
from sqlalchemy.orm import Session
from ..dependencies import user_oauth2
from ..models.attendance_models import ATMS_REPORT
from ..database.database import get_db
from ..schemas.attendance_schemas import AttendanceCreate


router = APIRouter(
    tags = ["Attendance Report"]
)

@router.post('/attendance_report')
def upload_attendance_report(attendance: AttendanceCreate,db:Session=Depends(get_db),):
# Create attendance record
    attendance_record = ATMS_REPORT(
        user_id=attendance.user_id,
        date=attendance.date,
        time_in=attendance.time_in,
        time_out=attendance.time_out,
        break_hours=attendance.break_hours,
        working_hours=attendance.working_hours,
    )
    
    db.add(attendance_record)
    db.commit()
    db.refresh(attendance_record)
    
    return {"message": "Attendance logged successfully", "data": attendance_record}