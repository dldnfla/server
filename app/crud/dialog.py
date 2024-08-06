from sqlalchemy.orm import Session

from .. import models, schemas


def create_dialog(db: Session, dialog: schemas.DialogCreate):
    db_dialog = models.Dialog(
        user_id=dialog.user_id, visitor=dialog.visitor, contents=dialog.contents
    )
    db.add(db_dialog)
    db.commit()
    db.refresh(db_dialog)

    return db_dialog


def get_dialog(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Dialog).slice(skip, limit).all()


def update_dialog(db: Session, dialog_id: int, dialog: schemas.DialogCreate):
    db.query(models.Dialog).filter(models.Dialog.id == dialog_id).update(dialog.dict())
    db.commit()
    db.refresh(db_dialog)

    return get_dialog
