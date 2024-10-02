from pydantic import BaseModel, Field,EmailStr
from datetime import date
from typing import Optional
from fastapi.encoders import jsonable_encoder
from .profile_picture_schemas import ProfilePic,ShowProfilePIc


class UserAccountDetail(BaseModel):
    Employee_ID: str 
    Official_Email_ID: EmailStr 
    First_Name: str 
    Last_Name: str
    Date_Of_Birth: date 
    Gender: str 
    Phone_Number: str 
    Role: str 
    # user_image: ShowProfilePIc

class Update_UserAccountDetail(BaseModel):
    # Employee_ID: Optional[str] = Field(default='20210002')
    # Official_Email_ID: Optional[EmailStr] = Field(default='sammy@gmail.com')
    First_Name: Optional[str] = Field(default='sam')
    Last_Name: Optional[str] = Field(default='Ella')
    Date_Of_Birth: Optional[date] = None 
    Gender: Optional[str] = Field(default='girl')
    Phone_Number: Optional[str] =  Field(default="13838494093")  
    Role: Optional[str] = Field(default='Frontend')


