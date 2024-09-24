#schemas for register
from pydantic import BaseModel, Field,EmailStr
from datetime import date
from typing import Optional


class UserSignUp(BaseModel):
    First_Name: str = Field(default='Precious')
    Last_Name: str = Field(default='Solomon')
    Date_Of_Birth: date = Field(default=date(2005, 2, 16))
    Gender: str = Field(default='girl')
    Onpassive_Email: EmailStr = Field(default='precious@gmail.com')
    password: str = Field(default='123htinx vh6^%^',min_length=7)
    confirm_password: str = Field(default='123htinx vh6^%^')
    Contact_No: int =  Field(default=12345678)  
    Role: str = Field(default='Backend')
    
    
class ShowUser(BaseModel):
    First_Name: str 
    Last_Name: str
    Date_Of_Birth: date 
    Gender: str 
    Onpassive_Email: EmailStr 
    Contact_No: int
    Role: str
    
    # serializing the data from orm to pydantic
    class Config:
        orm_mode = True