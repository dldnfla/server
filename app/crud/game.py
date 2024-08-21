from sqlalchemy.orm import Session

from .. import models, oauth2, schemas


def update_score(db: Session, new_score: schemas.ScoreCreate):
    db_score = get_score(db, username=new_score.username)

    if db_score is None:
        create_score(db, username=new_score.username, score=new_score.score)

    db.query(models.Score).filter(models.User.username == new_score.username).update(
        new_score.dict(exclude_unset=True)
    )
    db.commit()
    ...


def get_scorelist(db: Session):
    return (
        db.query(models.User.fullname, models.Score.score)
        .join(models.Score, models.User.username == models.Score.username)
        .order_by(models.Score.score)
        .limit(5)
        .all()
    )


def get_score(db: Session, username: str):
    return db.query(models.Score).filter(models.User.name == username).first()


def create_score(db: Session, score: schemas.ScoreCreate):
    db_score = models.Score(username=score.username, score=score.score)
    db.add(db_score)
    db.commit()
    db.refresh(db_score)
    return db_score

    ...
