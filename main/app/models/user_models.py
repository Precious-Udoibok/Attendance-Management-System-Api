#tables or models for login
from sqlalchemy import Column, Integer, String, Date, ForeignKey, Boolean
from ..database import database
from datetime import date


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
    Contact_No = Column(Integer)
    Role = Column(String)