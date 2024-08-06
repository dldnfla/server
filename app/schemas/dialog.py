from typing import List
from pydantic import BaseModel


class DialogBase(BaseModel):
    user_id: str
    visitor: str
    contents: str


class DialogCreate(DialogBase):
    pass

class DialogGet(DialogBase):
    id: int
    

class DialogEdit(DialogBase):
    id: int

    class Config:
        orm_mode: True
