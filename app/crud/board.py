from sqlalchemy.orm import Session

from .. import models, schemas


def create_post(db: Session, post: schemas.PostCreate, username: str):
    db_post = models.Board(
        username=username,
        tag=post.tag,
        title=post.title,
        contents=post.contents,
        date=post.date,
        link=post.link,
    )
    db.add(db_post)
    db.commit()
    db.refresh(db_post)

    return db_post


def get_all_posts(db: Session):
    return db.query(models.Board).all()


def get_post(db: Session, post_id: int):
    return db.query(models.Board).filter(models.Board.id == post_id).first()
