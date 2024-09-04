from sqlalchemy.orm import Session

from .. import models, schemas


def update_score(db: Session, new_score: schemas.ScoreCreate):
    db_score = get_score(db, username=new_score.username)

    if db_score is None:
        create_score(db, score=new_score)

    else:
        db.query(models.Score).filter(
            models.Score.username == new_score.username
        ).update(new_score.dict())
        db.commit()
    ...


def get_scorelist(db: Session, username: str):
    scorelist = (
        db.query(models.User.fullname, models.Score.score)
        .join(models.Score, models.User.username == models.Score.username)
        .filter(models.Score.username == username)
        .order_by(models.Score.score)
        .limit(5)
        .all()
    )

    return scorelist


def get_score(db: Session, username: str):
    return db.query(models.Score).filter(models.Score.username == username).all()


def create_score(db: Session, score: schemas.ScoreCreate):
    db_score = models.Score(username=score.username, score=score.score)
    db.add(db_score)
    db.commit()
    db.refresh(db_score)

    return db_score

    ...
