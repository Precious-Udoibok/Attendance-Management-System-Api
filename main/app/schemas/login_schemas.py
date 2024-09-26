#schemas for login
from pydantic import BaseModel, Field,EmailStr

class Login(BaseModel):
    Email_ID: EmailStr = Field(default='johndoe@gmail.com')
    Password: str = Field(default='12345&&&&894',min_length=7)