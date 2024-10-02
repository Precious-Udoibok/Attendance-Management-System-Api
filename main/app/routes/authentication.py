#this will contain the signup and login
from fastapi import APIRouter,status,Depends,HTTPException,Form
from ..database import database
from ..models import user_models
from passlib.context import CryptContext
from ..schemas import signup_schemas
from sqlalchemy.orm import Session
from typing import Annotated
from pydantic import EmailStr,Field
from datetime import timedelta
from ..dependencies import user_oauth2
# from ..models.user_models import Profile_Pictures

router = APIRouter(
    tags=['Signup/Login']
)

# the token will expire after 24 hours
ACCESS_TOKEN_EXPIRE_HOUR = 24

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


#signup
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
        First_Name =user.First_Name, Last_Name=user.Last_Name,
        Date_Of_Birth=user.Date_Of_Birth, 
        Onpassive_Email=user.Onpassive_Email, password=Hash.bcrypt(user.password), 
        Contact_No = user.Contact_No,
        Role = user.Role, Gender = user.Gender
    )
    
    
    # check if useremail already exist in the database
    existed_user = get_user_email(db, user.Onpassive_Email)
    if existed_user:
        raise HTTPException(
            status_code=409, detail="This email already exists"
            )
    
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    
    employee_unique_id = "KODE1" + str(new_user.id)
    
    # Create the Account details table when the user register
    new_user_account_details = user_models.UserAccount(
        Employee_ID= employee_unique_id ,  # Set the firstname from the User table
        Official_Email_ID=user.Onpassive_Email,
        First_Name=user.First_Name,
        Last_Name=user.Last_Name,  
        Gender = user.Gender,
        Phone_Number = user.Contact_No,
        Role = user.Role,
        # profile_pictures_id = new_user.id,
        user = new_user#default_profile_Pic
        )
    
    db.add(new_user_account_details)
    db.commit()
    db.refresh(new_user_account_details)

    
    # # check if the user entered the correct password
    # if user.password != user.confirm_password:
    #     raise HTTPException(status_code=400, detail="Passwords do not match")

    return new_user

@router.post('/login',
    summary="Login and generate JWT token with type and user id",
    description='''Authenticate a user by checking the email and password
    against the database. If valid,
    generate and return a JWT access token and type''',
    responses={404: {"description": "Invalid credentials or password"}}
             )

def user_login(Email_ID:Annotated[EmailStr,Form()], password:Annotated[str,Form()],
               db: Session = Depends(database.get_db)):
    """Get the useremail and password check it in the.
    database and create and return a jwt token"""
    # check if the username enter is in the database
    user_details = (
        db.query(user_models.User).filter(user_models.User.Onpassive_Email == Email_ID).first()
    )

    # if the user email is not in the database
    if not user_details:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Invalid Credentials"
        )

    # verify the password
    if not Hash.verify(user_details.password, password):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Invalid password"
        )

    user_id = user_details.id  # current user_id

    # if the useremail is in the database and the password is verified
    # set the time the token will exipre
    access_token_expire = timedelta(
        hours=ACCESS_TOKEN_EXPIRE_HOUR
    )  # then the user will have to login again
    # #generate the jwt token
    # #by passing in the data and the expire token time
    access_token = user_oauth2.create_access_token(
        data={"sub": Email_ID, "id": user_id}, expires_delta=access_token_expire
    )
    
    return {
        "token": access_token,
        "type": "bearer",
        "user_id": user_id,
    }

