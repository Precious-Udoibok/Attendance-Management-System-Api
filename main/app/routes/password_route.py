from fastapi import APIRouter, Depends, HTTPException,status
from ..schemas.password_schema import ChangePassword
from ..database import database
from sqlalchemy.orm import Session
from ..dependencies import user_oauth2
from ..models import user_models
from ..routes.authentication import Hash

router = APIRouter(
    tags= ['Password']
)

@router.post('/change_passsword')
def change_your_password(*,current_user=Depends(user_oauth2.get_current_user),
                         user_password: ChangePassword, db: Session=Depends(database.get_db)
                         ):
    
    person_id = db.query(user_models.User).filter(user_models.User.id == current_user).first()
    
    correct_old_password =  Hash.verify(person_id.password, user_password.old_password)
    # print(x)
    if not correct_old_password:
        raise HTTPException(status_code=status.HTTP_406_NOT_ACCEPTABLE,
                            detail = "Incorrect old password, enter the correct old password"
                            )
        
    if user_password.old_password == user_password.new_password:
        raise HTTPException(status_code=status.HTTP_406_NOT_ACCEPTABLE,
                            detail = "New password cannot be Old Password, Enter a different password"
                            )
        
    if user_password.confirm_newpassword != user_password.new_password:
        raise HTTPException(status_code=status.HTTP_406_NOT_ACCEPTABLE,
                            detail = "New Password must match Confirm New Password"
                            )
    hashed_new_password = Hash.bcrypt(user_password.new_password)
    person_id.password = hashed_new_password
    
    db.commit()
    print(person_id.password)
    return {'Message': 'Password Changed Successfully'}
    

    