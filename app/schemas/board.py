from typing import List, Optional
from pydantic import BaseModel


class PostBase(BaseModel):
    category: str
    title: str
    contents: str
    date: str
    link: str | None = None
    image: str | None = None


class PostCreate(PostBase):
    pass


class PostGet(PostBase):
    id: int


class PostEdit(BaseModel):
    category: str | None = None
    title: str | None = None
    contents: str | None = None
    date: str | None = None
    link: str | None = None
    image: str | None = None
    class Config:
        orm_mode: True
        from_attributes = True
