#store the users attendance report
from fastapi import APIRouter,Depends,HTTPException
from sqlalchemy.orm import Session
from ..dependencies import user_oauth2
from ..models.attendance_models import ATMS_REPORT
from ..database.database import get_db
from ..schemas.attendance_schemas import AttendanceCreate
from datetime import time, timedelta


router = APIRouter(
    tags = ["Attendance Report"]
)

@router.post('/upload_attendance_report')
def upload_attendance_report(attendance: AttendanceCreate, db:Session=Depends(get_db),
                             current_user=Depends(user_oauth2.get_current_user)
                             ):
# Create attendance record
    attendance_record = ATMS_REPORT(
        user_id=current_user,
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


@router.get('/get_attendance_report')
def get_attendance_report(db:Session=Depends(get_db),current_user=Depends(user_oauth2.get_current_user)):
    account_report = (
        db.query(ATMS_REPORT).filter(ATMS_REPORT.user_id == current_user).all()
    )
    if not account_report:
        raise HTTPException(status_code=404, detail="No Attendance Report yet")
    
    
    return account_report