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


def get_follow(db: Session, user_id: int, skip: int = 0, limit: int = 100):
    return (
        db.query(models.Follow)
        .filter(models.Follow.follower == user_id)
        .offset(skip)
        .limit(limit)
        .all()
    )


def update_follow(db: Session, new_qna: schemas.QnaEdit, user_id: str):
    db_qna = (
        db.query(models.Qna)
        .filter(models.Qna.user_id == user_id)
        .update(new_qna.model_dump())
    )

    db.commit()

    return get_follow(db, user_id)
