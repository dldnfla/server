from typing import List
from pydantic import BaseModel


class ScoreBase(BaseModel):
    username: str
    score: str


class ScoreCreate(ScoreBase):
    pass


class ScoreGet(ScoreBase):
    pass


class ScoreEdit(ScoreBase):
    pass

    class Config:
        orm_mode: True
        from_attributes = True
