from pydantic import BaseModel


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    username: str | None = None


class UserBase(BaseModel):
    username: str


class UserAuth(UserBase):
    hashed_password: str


class UserCreate(UserBase):
    password: str


class UserEdit(BaseModel):
    fullname: str | None = None
    profile_image: str | None = None
    status_message: str | None = None
    music_info: str | None = None

    class Config:
        orm_mode = True

class UserGet(BaseModel):
    id: int 
    username: str 
    fullname: str 
    profile_image: str 
    status_message: str 
    user_url: str
    music_info: str 

    class Config:
        orm_mode = True

