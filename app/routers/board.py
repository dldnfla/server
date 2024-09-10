from typing import Annotated, List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app import oauth2

from .. import crud, schemas, models
from ..database import get_db

router = APIRouter(prefix="/board", tags=["board"])


@router.post("/", status_code=status.HTTP_201_CREATED)
def create_post(
    current_user: Annotated[schemas.UserAuth, Depends(oauth2.get_authenticated_user)],
    post: schemas.PostCreate,
    db: Session = Depends(get_db),
):
    if current_user is None:
        raise HTTPException(status_code=404, detail="User not found")

    return crud.create_post(db, post, username=current_user.username)


# 모든 게시판 불러오기
@router.get("/", status_code=status.HTTP_200_OK)
def get_postlist(
    current_user: Annotated[schemas.UserAuth, Depends(oauth2.get_authenticated_user)],
    db: Session = Depends(get_db),
):
    return crud.get_all_posts(db)


# 목록에서 눌럿을 때 하나만 받아오는 거
@router.get("/{post_id}", status_code=status.HTTP_200_OK)
def get_post(
    current_user: Annotated[schemas.UserAuth, Depends(oauth2.get_authenticated_user)],
    post_id: int,
    db: Session = Depends(get_db),
):
    return crud.get_post(db, post_id=post_id)


# 태그별 게시글 목록 가지고 오기
@router.get("/category/{category}", status_code=status.HTTP_200_OK)
def get_post(
    current_user: Annotated[schemas.UserAuth, Depends(oauth2.get_authenticated_user)],
    category: str,
    db: Session = Depends(get_db),
):
    return crud.get_post_category(db, category=category)


@router.get("/location/{location}", status_code=status.HTTP_200_OK)
def get_post_by_location(
    current_user: Annotated[schemas.UserAuth, Depends(oauth2.get_authenticated_user)],
    location: str,
    db: Session = Depends(get_db),
):
    return crud.get_post_by_location(db, location)


# 제목 검색
@router.get("/search/{title}", status_code=status.HTTP_200_OK)
def get_post(
    current_user: Annotated[schemas.UserAuth, Depends(oauth2.get_authenticated_user)],
    title: str,
    db: Session = Depends(get_db),
):
    return crud.search_posts(db, title)
