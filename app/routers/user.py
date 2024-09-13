from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from .. import crud, oauth2, schemas
from ..database import get_db

router = APIRouter(prefix="/api/users", tags=["users"])


@router.post(
    "/signup",
    response_model=schemas.UserGet,
    status_code=status.HTTP_201_CREATED,
)
def create_user(
    user: schemas.UserCreate,
    db: Session = Depends(get_db),
):
    db_user = crud.get_user_by_username(db, username=user.username)

    if db_user:
        raise HTTPException(status_code=400, detail="User already registered")

    return crud.create_user(
        db=db,
        user=schemas.UserCreate(
            username=user.username,
            password=user.password,
            fullname=user.fullname,
        ),
    )


@router.post("/duplicate", status_code=status.HTTP_200_OK)
def check_duplicate_user(
    username: str,
    db: Session = Depends(get_db),
):
    db_user = crud.get_user_by_username(db, username=username)

    if db_user:
        raise HTTPException(status_code=400, detail="ID already registered")

    ...


@router.get("/me", response_model=schemas.UserGet)
def get_user(
    current_user: Annotated[schemas.UserGet, Depends(oauth2.get_authenticated_user)],
):
    if current_user is None:
        raise HTTPException(status_code=404, detail="User not found")

    return current_user


@router.get("/redirection")
def get_redirection_page(username: str, db: Session = Depends(get_db)):
    db_user = crud.get_user_by_username(db, username)
    db_user_dialog = crud.get_dialog(db, db_user.id)
    db_user_following = crud.get_follow(db, username)
    db_user_get_qna = crud.get_qna(db, db_user.id)
    db_user_game = crud.get_scorelist(db, username)
    db_user_video = crud.get_video(db, db_user.id)

    return {
        "user": db_user,
        "dialog": db_user_dialog,
        "following": db_user_following,
        "qna": db_user_get_qna,
        "game_scores": db_user_game,
        "video": db_user_video,
    }


@router.put("/update", response_model=schemas.UserGet)
def update_user(
    new_user: schemas.UserEdit,
    current_user: Annotated[schemas.UserGet, Depends(oauth2.get_authenticated_user)],
    db: Session = Depends(get_db),
):
    if current_user is None:
        raise HTTPException(status_code=404, detail="User not found")

    return crud.update_user(db, new_user, current_user)
