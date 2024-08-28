from typing import Annotated, List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app import oauth2

from .. import crud, schemas
from ..database import get_db

router = APIRouter(prefix="/board", tags=["board"])


@router.post("/", response_model=schemas.BoardGet, status_code=status.HTTP_201_CREATED)
def create_post(
    current_user: Annotated[schemas.UserAuth, Depends(oauth2.get_authenticated_user)],
    board: schemas.BoardCreate,
    db: Session = Depends(get_db),
):
    if current_user is None:
        raise HTTPException(status_code=404, detail="User not found")

    return crud.create_board(db, board, user_id=current_user.id)


# 모든 게시판 불러오기
@router.get("/", response_model=List[schemas.BoardGet], status_code=status.HTTP_200_OK)
def get_postlist(
    current_user: Annotated[schemas.UserAuth, Depends(oauth2.get_authenticated_user)],
    db: Session = Depends(get_db),
):
    if current_user is None:
        raise HTTPException(status_code=404, detail="User not found")

    return crud.get_all_boards(db)


# 목록에서 눌럿을 때 하나만 받아오는 거
@router.get(
    "/{board_id}", response_model=schemas.BoardGet, status_code=status.HTTP_200_OK
)
def get_post(
    current_user: Annotated[schemas.UserAuth, Depends(oauth2.get_authenticated_user)],
    board_id: int,
    db: Session = Depends(get_db),
):
    if current_user is None:
        raise HTTPException(status_code=404, detail="User not found")

    return crud.get_board(db, board_id=board_id)


# 태그별 게시글 목록 가지고 오기
# 제목 검색
