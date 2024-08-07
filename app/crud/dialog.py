from sqlalchemy.orm import Session

from .. import models, schemas


def create_dialog(db: Session, dialog: schemas.DialogCreate):
    db_dialog = models.Dialog(
        user_id=dialog.user_id, 
        visitor=dialog.visitor, 
        contents=dialog.contents,
    )
    db.add(db_dialog)
    db.commit()
    db.refresh(db_dialog)

    return db_dialog


def get_dialog(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Dialog).slice(skip, limit).all()

# 특정 유저의 방명록 목록만 가지고 와야되는 거라 user_id로 필터 걸어야됨

def get_dialog(db: Session, user_id: int, skip: int = 0, limit: int = 100):
    return db.query(models.Dialog).filter(models.Dialog.user_id == user_id).offset(skip).limit(limit).all()


def update_dialog(db: Session, dialog_id: int, dialog: schemas.DialogCreate):
    db.query(models.Dialog).filter(models.Dialog.id == dialog_id).update(dialog.dict())
    db.commit()

    return get_dialog
