from sqlalchemy.orm import Session

from .. import models, schemas


def create_board(db: Session, board: schemas.BoardCreate, user_id=int):
    db_board = models.Board(
        tag=board.tag,
        title=board.title,
        contents=board.contents,
        date=board.date,
        link=board.link,
        images=board.images,
        user_id=user_id,
    )
    db.add(db_board)
    db.commit()
    db.refresh(db_board)

    return db_board


def get_all_boards(db: Session):
    return db.query(models.Board).all()


def get_board(db: Session, board_id: int):
    return db.query(models.Board).filter(models.Board.id == board_id).first()
