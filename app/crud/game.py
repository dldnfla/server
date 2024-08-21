from sqlalchemy.orm import Session

from .. import models, oauth2, schemas


def update_score(db: Session, score: schemas.ScoreCreate):
    db.query(models.User).filter(models.User.username == score.username).update(
        score.dict(exclude_unset=True)
    )
    db.commit()

    ...


def get_user(db: Session, user_id: int):
    return db.query(models.User).filter(models.User.id == user_id).first()


def get_user_by_username(db: Session, username: str):
    return db.query(models.User).filter(models.User.username == username).first()


def update_user(db: Session, new_user: schemas.UserEdit, user: schemas.UserGet):
    db.query(models.User).filter(models.User.id == user.id).update(
        new_user.dict(exclude_unset=True)
    )
    db.commit()

    return get_user(db, user.id)
