#routes for account details
from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from ..models import user_models
from ..dependencies import user_oauth2
from ..schemas.account_details_schema import UserAccountDetail
from ..database.database import get_db

router = APIRouter(
    tags= ['Account Details']
)

@router.get('/account_details')
def get_account_details(current_user=Depends(user_oauth2.get_current_user), db: Session = Depends(get_db)):
    account_details = (
        db.query(user_models.UserAccount).filter(user_models.UserAccount.id == current_user).first()
    )
    if not account_details:
        raise HTTPException(status_code=404, detail="Personal info not found")
    return account_details
