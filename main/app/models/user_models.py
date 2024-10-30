#tables or models for login
from sqlalchemy import Column, Integer, String, Date, ForeignKey, Boolean
from ..database import database
from datetime import date
from sqlalchemy.orm import relationship


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
    Onpassive_Email = Column(String, unique=True)
    password = Column(String)
    Contact_No = Column(String)
    Role = Column(String)
    
    account_details = relationship("UserAccount", back_populates="user")
    
    
class UserAccount(database.Base):
    __tablename__ = "AMS_user_details"
    
    id = Column(Integer, primary_key=True, index=True)
    Employee_ID = Column(String, unique=True)  # Make sure this is defined
    Official_Email_ID = Column(String, ForeignKey("AMS_users.Onpassive_Email"), unique=True)
    # profile_pictures_id = Column(Integer,ForeignKey("profile_pictures.id"), unique=True)
    First_Name= Column(String)
    Last_Name = Column(String)
    Date_Of_Birth = Column(Date, default=date(2005, 10, 12))
    Gender = Column(String)
    Phone_Number = Column(String)
    Role = Column(String)
    
    user = relationship("User", back_populates="account_details")
    # user_image = relationship("Profile_Pictures", back_populates="image")  
    
    
# class Profile_Pictures(database.Base):
#     __tablename__ = "profile_pictures"

#     id = Column(Integer, primary_key=True)
#     picture_url = Column(String, default = "https://res.cloudinary.com/drof2shjx/image/upload/v1727784456/attendenace_profile_pics/1.jpg", 
#                          nullable=True)
    
#     image = relationship("UserAccount", back_populates="user_image")
