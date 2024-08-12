from typing import List
from pydantic import BaseModel


class WishBase(BaseModel):
    username: str
    contents: str


class WishCreate(WishBase):
    pass

class WishEdit(WishBase):

    class Config:
        orm_mode: True