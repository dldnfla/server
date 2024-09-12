from typing import Annotated
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app import oauth2

from .. import crud, schemas
from ..database import get_db

router = APIRouter(prefix="/api/qna", tags=["qna"])


@router.get("/", status_code=status.HTTP_200_OK)
def get_qna(
    current_user: Annotated[schemas.UserAuth, Depends(oauth2.get_authenticated_user)],
    skip: int = 0,
    limit: int = 30,
    db: Session = Depends(get_db),
):
    if current_user is None:
        raise HTTPException(status_code=404, detail="User not found")

    return crud.get_qna(db, user_id=current_user.id, skip=skip, limit=limit)


@router.put("/", status_code=status.HTTP_200_OK)
def put_qna(
    current_user: Annotated[schemas.UserAuth, Depends(oauth2.get_authenticated_user)],
    qna: schemas.QnaEdit,
    db: Session = Depends(get_db),
):
    if current_user is None:
        raise HTTPException(status_code=404, detail="User not found")

    return crud.update_qna(db, qna, user_id=current_user.id)
