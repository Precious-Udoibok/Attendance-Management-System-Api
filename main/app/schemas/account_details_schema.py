from pydantic import BaseModel, Field,EmailStr
from datetime import date
from typing import Optional


class UserAccountDetail(BaseModel):
    Employee_ID: str = Field(default='20210002')
    Official_Email_ID: EmailStr = Field(default='sammy@gmail.com')
    First_Name: str = Field(default='sam')
    Last_Name: str = Field(default='Ella')
    Date_Of_Birth: date = Field(default=date(2005, 2, 16))
    Gender: str = Field(default='girl')
    Phone_Number: str =  Field(default="13838494093")  
    Role: str = Field(default='Frontend')
    Branch: str = Field(default='Uyo(Eket)')
    Address: str = Field(default='28 AfahaEket')
    Joined_Date: date = Field(default=date(2005, 2, 16))
    
