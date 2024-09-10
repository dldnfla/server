from sqlalchemy.orm import Session

from .. import models, schemas


def create_post(db: Session, post: schemas.PostCreate, username: str):
    db_post = models.Board(
        username=username,
        category=post.category,
        location=post.location,
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
    posts = (
        db.query(models.Board, models.User.fullname)
        .join(models.User, models.User.username == models.Board.username)
        .all()
    )

    result = []
    for board, fullname in posts:
        board.username = fullname
        result.append(board)

    return result


def get_post(db: Session, post_id: int):
    db_post = db.query(models.Board).filter(models.Board.id == post_id).first()

    if db_post:
        db_post.views += 1
        db.commit()
        db.refresh(db_post)

        post = (
            db.query(models.Board, models.User.fullname)
            .join(models.User, models.User.username == models.Board.username)
            .filter(models.Board.id == post_id)
            .first()
        )

        # first -> 단일객체 : 반복문 불가
        if post:
            board, fullname = post
            board.username = fullname
            return board

    return None


def get_post_category(db: Session, category: str):
    valid_categories = ["일상", "맛집"]

    if category in valid_categories:
        post = (
            db.query(models.Board, models.User.fullname)
            .join(models.User, models.User.username == models.Board.username)
            .filter(models.Board.category == category)
            .all()
        )
        result = []
        for board, fullname in post:
            board.username = fullname
            result.append(board)

        return result
    else:
        return []


def get_post_by_location(db: Session, location: str):
    valid_locations = ["서울", "강릉", "제주", "부산", "대구", "대전", "기타"]

    if location in valid_locations:
        posts = (
            db.query(models.Board, models.User.fullname)
            .join(models.User, models.User.username == models.Board.username)
            .filter(models.Board.location == location)
            .all()
        )
        result = []

        for board, fullname in posts:
            board.username = fullname
            result.append(board)

        return result
    else:
        return []


def update_post(db: Session, new_post: str, post_id):
    db_post = (
        db.query(models.Board)
        .filter(models.Board.id == post_id)
        .update({"image": new_post})
    )

    db.commit()

    return db_post


def search_posts(db: Session, title: str):
    posts = (
        db.query(models.Board, models.User.fullname)
        .join(models.User, models.User.username == models.Board.username)
        .filter(models.Board.title.like(f"%{title}%"))
        .offset(0)
        .limit(10)
        .all()
    )

    result = []
    for board, fullname in posts:
        board.username = fullname
        result.append(board)

    return result
