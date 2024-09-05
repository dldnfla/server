from typing import Annotated
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app import oauth2

from .. import crud, schemas, models
from ..database import get_db

router = APIRouter(prefix="/score", tags=["game"])


@router.put("/", status_code=status.HTTP_201_CREATED)
def update_score(
    current_user: Annotated[schemas.UserAuth, Depends(oauth2.get_authenticated_user)],
    new_score: schemas.ScoreCreate,
    db: Session = Depends(get_db),
):
    return crud.update_score(db, new_score, username=current_user.username)


@router.get("/", status_code=status.HTTP_200_OK)
def get_scorelist(
    current_user: Annotated[schemas.UserAuth, Depends(oauth2.get_authenticated_user)],
    db: Session = Depends(get_db),
):
    return crud.get_scorelist(db, username=current_user.username)


@router.get("/me", status_code=status.HTTP_200_OK)
def get_score(
    current_user: Annotated[schemas.UserAuth, Depends(oauth2.get_authenticated_user)],
    db: Session = Depends(get_db),
):
    return crud.get_score(db, username=current_user.username)
