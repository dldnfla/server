from typing import List
from pydantic import BaseModel


class QnaBase(BaseModel):
    answer1: str | None = None
    answer2: str | None = None
    answer3: str | None = None
    answer4: str | None = None
    answer5: str | None = None
    answer6: str | None = None
    answer7: str | None = None
    answer8: str | None = None
    answer9: str | None = None
    answer10: str | None = None


class QnaCreate(QnaBase):
    pass


class QnaEdit(QnaBase):

    class Config:
        orm_mode: True
