from sqlalchemy.orm import Session

from .. import models, schemas


def create_wish(db: Session, wish: schemas.WishCreate):
    db_wish = models.Wish(
        username=wish.username,
        contents=wish.contents,
    )
    db.add(db_wish)
    db.commit()
    db.refresh(db_wish)

    return db_wish


def get_wish(db: Session, skip: int = 0, limit: int = 100):
    return (
        db.query(models.Wish)
        .offset(skip)
        .limit(limit)
        .all()
    )
