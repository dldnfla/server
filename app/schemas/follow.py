from typing import List
from pydantic import BaseModel


class FollowBase(BaseModel):
    follower: str
    followee: str
    follow_get: bool


class FollowCreate(FollowBase):
    pass


class FollowGet(FollowBase):
    id: int


class FollowEdit(FollowBase):
    class Config:
        orm_mode: True
        from_attributes = True
