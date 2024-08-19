from typing import List
from pydantic import BaseModel


class MusicBase(BaseModel):
    singer: str
    music_title: str
    music_info: str


class MusicCreate(MusicBase):
    pass


class MusicGet(MusicBase):
    id: int


class MusicEdit(MusicBase):
    class Config:
        orm_mode: True
        from_attributes = True
