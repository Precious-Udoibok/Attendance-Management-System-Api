from pydantic import BaseModel
from typing import Optional

class ProfilePic(BaseModel):
    user_image: Optional[str]
    
    
class ShowProfilePIc(BaseModel):
    picture_url: Optional[str]
   
    class Config:
        orm_mode = True