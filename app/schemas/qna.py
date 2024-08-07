from typing import List
from pydantic import BaseModel


class QnaBase(BaseModel):
    answer1: str
    answer2: str
    answer3: str
    answer4: str
    answer5: str
    answer6: str
    answer7: str
    answer8: str
    answer9: str
    answer10: str


class QnaCreate(QnaBase):
    pass


class QnaEdit(QnaBase):
    id: int

    class Config:
        orm_mode: True
