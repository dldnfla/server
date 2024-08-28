from sqlalchemy.orm import Session

from .. import models, schemas


def create_post(db: Session, board: schemas.BoardCreate, user_id=int):
    db_board = models.Board(
        tag=board.tag,
        title=board.title,
        contents=board.contents,
        date=board.date,
        link=board.link,
        image=board.images,
        user_id=user_id,
    )
    db.add(db_board)
    db.commit()
    db.refresh(db_board)

    return db_board


def get_all_posts(db: Session):
    return db.query(models.Board).all()


def get_post(db: Session, board_id: int):
    return db.query(models.Board).filter(models.Board.id == board_id).first()
