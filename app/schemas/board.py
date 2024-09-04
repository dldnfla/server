from typing import List, Optional
from pydantic import BaseModel


class PostBase(BaseModel):
    tag: str
    title: str
    contents: str
    date: str
    link: str | None = None
    image: str | None = None


class PostCreate(PostBase):
    pass


class PostGet(PostBase):
    id: int


class PostEdit(PostBase):
    class Config:
        orm_mode: True
        from_attributes = True
