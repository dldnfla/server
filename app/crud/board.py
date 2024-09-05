from sqlalchemy.orm import Session

from .. import models, schemas


def create_post(db: Session, post: schemas.PostCreate, username: str):
    db_post = models.Board(
        username=username,
        category=post.category,
        title=post.title,
        contents=post.contents,
        date=post.date,
        link=post.link,
        image=post.image,
    )
    db.add(db_post)
    db.commit()
    db.refresh(db_post)

    return db_post


def get_all_posts(db: Session):
    return db.query(models.Board).all()


def get_post(db: Session, post_id: int):
    post = db.query(models.Board).filter(models.Board.id == post_id).first()

    if post:
        post.views += 1
        db.commit()
        db.refresh(post)
        return post
    return None


def get_post_category(db: Session, category: str):
    return db.query(models.Board).filter(models.Board.category == category).all()

def update_post(db: Session, new_post: str,post_id):
    db_post = (
        db.query(models.Board)
        .filter(models.Board.id == post_id)
        .update( {"image": new_post})
    )

    db.commit()

    return db_post
