# This will conatin the user picture tables
from sqlalchemy import Column, String , Integer,ForeignKey
from ..database import database
# from .user_models import UserAccount

class Profile_Pictures(database.Base):
    __tablename__ = "profile_pictures"

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, unique=True)
    picture_url = Column(String, default = "https://res.cloudinary.com/drof2shjx/image/upload/v1727784456/attendenace_profile_pics/1.jpg", 
                         nullable=True)
    
    # image = relationship("UserAccount", back_populates="user_image")