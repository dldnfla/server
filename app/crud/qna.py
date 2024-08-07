from sqlalchemy.orm import Session

from .. import models, schemas

def create_qna(db: Session, qna: schemas.QnaCreate):
    db_qna = models.Qna(**qna.dict())
    db.add(db_qna)
    db.commit()
    db.refresh(db_qna)
    return db_qna

def get_qna(db: Session, user_id: str, skip: int = 0, limit: int = 30):
    return (
        db.query(models.Qna)
        .filter(models.Qna.user_id == user_id)
        .offset(skip)
        .limit(limit)
        .all()
    )


def update_qna(db: Session, new_qna: schemas.QnaEdit, user_id: str):
    db_qna = (
        db.query(models.Qna)
        .filter(models.Qna.user_id == user_id)
        .updaate(new_qna.dict())
    )

    db.commit()

    return get_qna(db, new_qna)
