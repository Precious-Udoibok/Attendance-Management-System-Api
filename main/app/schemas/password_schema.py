from pydantic import BaseModel

class ChangePassword(BaseModel):
    old_password: str
    new_password: str
    confirm_newpassword:str