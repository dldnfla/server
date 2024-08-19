from sqlalchemy.orm import Session

from .. import models, schemas


def create_qna(db: Session, qna: schemas.QnaCreate):
    db_qna = models.Qna(**qna.dict())
    db.add(db_qna)
    db.commit()
    db.refresh(db_qna)
    return db_qna


def get_qna(db: Session, user_id: int):
    return db.query(models.Qna).filter(models.Qna.user_id == user_id).all()


def update_qna(db: Session, new_qna: schemas.QnaEdit, user_id: int):
    db_qna = db.query(models.Qna).filter(models.Qna.user_id == user_id).first()

    if db_qna is None:
        db_qna = models.Qna(
            user_id=user_id,
            answer1="",
            answer2="",
            answer3="",
            answer4="",
            answer5="",
            answer6="",
            answer7="",
            answer8="",
            answer9="",
            answer10="",
        )
        db.add(db_qna)
        db.commit()
        db.refresh(db_qna)

    db_qna = (
        db.query(models.Qna)
        .filter(models.Qna.user_id == user_id)
        .update(new_qna.model_dump())
    )

    db.commit()

    return get_qna(db, user_id)
