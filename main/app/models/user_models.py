#tables or models for login
from sqlalchemy import Column, Integer, String, Date, ForeignKey, Boolean
from ..database import database
from datetime import date

dob = date(2005, 10, 12)

# Convert to MM/DD/YYYY format for display
formatted_dob = dob.strftime('%m/%d/%Y')

# User Model
class User(database.Base):
    __tablename__ = "AMS_users"

    id = Column(Integer, primary_key=True, index=True)
    First_Name = Column(String)
    Last_Name = Column(String)
    Date_Of_Birth= Column(Date, default=date(2005, 10, 12))
    Gender = Column(String)
    Onpassive_Email = Column(String)
    password = Column(String)
    Contact_No = Column(String)
    Role = Column(String)
    
class UserAccount(database.Base):
    __tablename__ = "AMS_user_details"
    
    id = Column(Integer, primary_key=True, index=True)
    Employee_ID = Column(String)
    Official_Email_ID = Column(String)
    First_Name= Column(String)
    Last_Name = Column(String)
    Date_Of_Birth = Column(Date, default=date(2005, 10, 12))
    Gender = Column(String)
    Phone_Number = Column(String)
    Shift_Time = Column(String)
    Role = Column(String)
    Branch = Column(String)
    Address = Column(String)
    Joined_Date = Column(String)
    