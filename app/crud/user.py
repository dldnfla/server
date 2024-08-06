from sqlalchemy.orm import Session

from .. import models, oauth2, schemas


def create_user(db: Session, user: schemas.UserCreate):
    db_user = models.User(
        username=user.username,
        hashed_password=oauth2.get_password_hash(user.password),
    )

    db.add(db_user)
    db.commit()
    db.refresh(db_user)

    return db_user


def get_user(db: Session, user_id: int):
    return db.query(models.User).filter(models.User.id == user_id).first()


def get_user_by_username(db: Session, username: str):
    return db.query(models.User).filter(models.User.username == username).first()


def update_user(db: Session, user: schemas.UserGet, new_user: schemas.UserEdit):
    db.query(models.User).filter(models.User.id == user.id).update(new_user.dict())
    db.commit()

    return get_user(db, user.id)
