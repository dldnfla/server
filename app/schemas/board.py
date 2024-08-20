from typing import List, Optional
from pydantic import BaseModel


class BoardBase(BaseModel):
    tag: str
    title: str
    contents: str
    date: str
    link: Optional[str] = None
    images: Optional[List[str]] = None


class BoardCreate(BoardBase):
    pass


class BoardGet(BoardBase):
    id: int


class BoardEdit(BoardBase):
    class Config:
        orm_mode: True
        from_attributes = True
