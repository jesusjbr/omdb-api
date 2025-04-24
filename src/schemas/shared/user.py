from pydantic import BaseModel


class UserData(BaseModel):
    username: str
    hashed_password: str
    is_admin: bool

    class Config:
        from_attributes = True
