from typing import List
from pydantic import BaseModel


class DialogBase(BaseModel):
    user_id: int
    visitor: str
    contents: str


class DialogCreate(DialogBase):
    pass


class DialogGet(DialogBase):
    id: int


class DialogEdit(DialogBase):
    class Config:
        orm_mode: True
        from_attributes = True
