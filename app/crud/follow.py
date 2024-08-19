from typing import Annotated
from fastapi import Depends, HTTPException
from sqlalchemy.orm import Session

from app import oauth2

from .. import models, schemas


def create_follow(db: Session, follow: schemas.FollowCreate):
    db_followee = (
        db.query(models.User).filter(models.User.username == follow.followee).first()
    )

    if db_followee is None:
        raise HTTPException(status_code=404, detail="User not found")

    db_follow = models.Follow(
        follower=follow.follower,
        followee=follow.followee,
    )
    db.add(db_follow)
    db.commit()
    db.refresh(db_follow)

    return db_follow


def get_follow(
    db: Session,
    username: str,
    skip: int = 0,
    limit: int = 100,
):
    follower_list = (
        db.query(models.Follow)
        .filter(
            (models.Follow.follower == username) | (models.Follow.followee == username),
            models.Follow.follow_get == 1,
        )
        .offset(skip)
        .limit(limit)
        .all()
    )

    return follower_list


def get_follow_request(db: Session, username: str):
    return db.query(models.Follow).filter(models.Follow.followee == username, models.Follow.follow_get == False).all()


def check_follow_request(db: Session, follower: str, followee: str):
    db_follow_request = (
        db.query(models.Follow)
        .filter(
            models.Follow.follower == follower,
            models.Follow.followee == followee,
        )
        .first()
    )

    return db_follow_request


def update_follow(db: Session, follow: schemas.FollowEdit, username: str):
    db.query(models.Follow).filter(
        models.Follow.follower == follow.follower,
        models.Follow.followee == username,
    ).update(follow.dict())

    db.commit()

    return get_follow(db, username=username)
