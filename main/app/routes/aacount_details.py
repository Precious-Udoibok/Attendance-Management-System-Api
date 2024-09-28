#routes for account details
from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from ..models import user_models
from ..dependencies import user_oauth2
from ..schemas.account_details_schema import UserAccountDetail,Update_UserAccountDetail
from ..database.database import get_db


router = APIRouter(
    tags= ['Account Details']
)

@router.get('/get_account_details',response_model=UserAccountDetail)
def get_account_details(current_user=Depends(user_oauth2.get_current_user), db: Session = Depends(get_db)):
    print(current_user)
    account_details = (
        db.query(user_models.UserAccount).filter(user_models.UserAccount.id == current_user).first()
    )
    if not account_details:
        raise HTTPException(status_code=404, detail="Personal info not found")
    return account_details

@router.put('/update_account_details')
def get_account(
    account_details_update_schema: Update_UserAccountDetail,
    current_user=Depends(user_oauth2.get_current_user),
    db: Session = Depends(get_db),token=Depends(get_db)
):
    account_details_update = db.query(user_models.UserAccount).filter(
        user_models.UserAccount.id == current_user
    )
    json_data = account_details_update_schema
    # update the account details to the user project
    account_details_update.update(json_data.dict())
    db.commit()
    return json_data

