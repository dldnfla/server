from sqlalchemy.orm import Session

from .. import models, schemas


def get_qna(db: Session, user_id: str, skip: int = 0, limit: int = 30):
    return db.query(models.Qna).filter(models.Qna.user_id == user_id).offset(skip).limit(limit).all()


def update_qna(db: Session, qna: schemas.QnaCreate, user_id: str):
    db_qna = db.query(models.Qna).filter(models.Qna.user_id == user_id).first()
    
    for key, value in qna.dict().items():
        setattr(db_qna, key, value)
        
    db.commit()

    return get_qna
