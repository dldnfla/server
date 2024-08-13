from typing import List
from pydantic import BaseModel


class MailboxBase(BaseModel):
    title: str
    recipient: str
    sender: str
    content: str
    date: str


class MailboxCreate(MailboxBase):
    pass

class MailboxEdit(MailboxBase):

    class Config:
        orm_mode: True