from sqlalchemy.orm import Session

from .. import models, oauth2, schemas


def update_score(db: Session, score: schemas.ScoreCreate):
    db_score = get_score(db,username = score.username)

    if db_score is None:
        create_score(db,username=score.username,score=score.score)

    ...


def create_score(db: Session, score: schemas.ScoreCreate):
    db_score = models.Score(
        username = score.username,
        score = score.score
    )
    db.add(db_score)
    db.commit()
    db.refresh(db_score)
    return db_score

    ...

def get_score(db: Session, username: str):
    return db.query(models.Score).filter(models.User.name== username).first()


def update_user(db: Session, new_user: schemas.UserEdit, user: schemas.UserGet):
    db.query(models.User).filter(models.User.id == user.id).update(
        new_user.dict(exclude_unset=True)
    )
    db.commit()

    return get_user(db, user.id)
