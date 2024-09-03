from typing import List
from pydantic import BaseModel


class ScoreBase(BaseModel):
    username: str


class ScoreCreate(ScoreBase):
    score: int


class ScoreGet(ScoreBase):
    pass


class ScoreEdit(ScoreBase):
    score: int

    class Config:
        orm_mode: True
        from_attributes = True
