from sqlalchemy.orm import Session

from sqlalchemy import desc
from .. import models, schemas


def update_score(db: Session, new_score: schemas.ScoreCreate, username: str):
    db_score = get_score(db, username=username)

    if db_score is None:
        create_score(db, score=new_score, username=username)

    else:
        if db_score.score > new_score.score:
            pass

        else:
            db.query(models.Score).filter(models.Score.username == username).update(
                {"score": new_score.score}
            )
            db.commit()

    return get_score(db, username=username)

    ...


def get_scorelist(db: Session, username: str):
    scorelist = (
        db.query(models.User.fullname, models.Score.score)
        .join(models.Score, models.User.username == models.Score.username)
        .order_by(desc(models.Score.score))
        .limit(5)
        .all()
    )

    return scorelist


def get_score(db: Session, username: str):
    return db.query(models.Score).filter(models.Score.username == username).first()


def create_score(db: Session, score: schemas.ScoreCreate, username: str):
    db_score = models.Score(username=username, score=score.score)
    db.add(db_score)
    db.commit()
    db.refresh(db_score)

    return db_score

    ...
