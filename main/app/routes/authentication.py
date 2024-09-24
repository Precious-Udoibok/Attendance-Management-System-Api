#this will contain the signup and login
from fastapi import APIRouter,status,Depends,HTTPException
from ..database import database
from ..models import user_models
from passlib.context import CryptContext
from ..schemas import signup_schemas
from sqlalchemy.orm import Session

router = APIRouter(
    tags=['Signup/Login']
)

# encyrpt the user password

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


class Hash:
    def bcrypt(password: str):
        return pwd_context.hash(password)

    # verify the password
    def verify(hashed_password, plain_password):
        return pwd_context.verify(plain_password, hashed_password)


# function to get user email
def get_user_email(db, email):
    user = db.query(user_models.User).filter(
        user_models.User.Onpassive_Email == email).first()
    return user



@router.post('/register',
    status_code=status.HTTP_201_CREATED,
    response_model=signup_schemas.ShowUser,
    summary="Enables the User to create a new account(Register)",
    description="Create a new user and add it to the database",
    response_description='''Returns a successful created.
    message and status code of 201'''
             )
def register(user:signup_schemas.UserSignUp, db: Session=Depends(database.get_db)):
    new_user = user_models.User(
        First_Name =user.First_Name, Last_Name=user.Last_Name, Date_Of_Birth=user.Date_Of_Birth, 
        Onpassive_Email=user.Onpassive_Email, password=Hash.bcrypt(user.password), Contact_No = user.Contact_No,
        Role = user.Role, Gender = user.Gender
    )

    # check if the user entered the correct password
    if user.password != user.confirm_password:
        raise HTTPException(status_code=400, detail="Passwords do not match")

    # check if useremail already exist in the database
    existed_user = get_user_email(db, user.Onpassive_Email)
    if existed_user:
        raise HTTPException(
            status_code=409, detail="This email already exists"
            )

    db.add(new_user)
    db.commit()
    db.refresh(new_user)


    return new_user