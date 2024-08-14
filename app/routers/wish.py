from typing import Annotated
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app import oauth2

from .. import crud, schemas
from ..database import get_db

router = APIRouter(prefix="/wish", tags=["wish"])


@router.post("/", status_code=status.HTTP_201_CREATED)
def create_wish(
    wish: schemas.WishCreate,
    db: Session = Depends(get_db),
):
    return crud.create_wish(db, wish)


@router.get("/", status_code=status.HTTP_200_OK)
def get_wish(
    current_user: Annotated[schemas.UserAuth, Depends(oauth2.get_authenticated_user)],
    skip: int = 0,
    limit: int = 30,
    db: Session = Depends(get_db),
):
    if current_user is None:
        raise HTTPException(status_code=404, detail="User not found")

    return crud.get_wish(db, skip=skip, limit=limit)
