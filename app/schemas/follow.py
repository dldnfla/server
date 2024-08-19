from typing import List
from pydantic import BaseModel


class FollowBase(BaseModel):
    follower: str
    followee: str


class FollowCreate(FollowBase):
    pass


class FollowGet(FollowBase):
    id: int


class FollowEdit(FollowBase):
    follow_get: bool | None = True

    class Config:
        orm_mode: True
        from_attributes = True
