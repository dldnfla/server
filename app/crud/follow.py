from sqlalchemy.orm import Session

from .. import models, schemas


def create_follow(db: Session, follow: schemas.FollowCreate):
    db_follow = models.Follow(
        follower=follow.follower,
        followee=follow.followee,
    )
    db.add(db_follow)
    db.commit()
    db.refresh(db_follow)

    return db_follow


def get_follow(db: Session, user_id: str, skip: int = 0, limit: int = 100):
    return (
        db.query(models.Follow)
        # .filter(models.Follow.follower == user_id, models.Follow.follow_get == True)
        .offset(skip)
        .limit(limit)
        .all()
    )


def update_follow(db: Session, follow: schemas.FollowEdit, user_id: str):
    db.query(models.Follow).filter(
        models.Follow.follower == user_id, models.Follow.followee == follow.followee
    ).update(follow.dict(exclude_unset=True))

    db.commit()

    return get_follow(db, user_id)
