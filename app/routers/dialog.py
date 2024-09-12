from typing import Annotated
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app import oauth2

from .. import crud, schemas
from ..database import get_db

router = APIRouter(prefix="/api/dialog", tags=["dialog"])


@router.post("/", response_model=schemas.DialogGet, status_code=status.HTTP_201_CREATED)
def create_dialog(
    dialog: schemas.DialogCreate,
    db: Session = Depends(get_db),
):
    if dialog.user_id is None:
        raise HTTPException(status_code=404, detail="User not found")

    return crud.create_dialog(db, dialog)


@router.get("/", status_code=status.HTTP_200_OK)
def get_dialog(
    current_user: Annotated[schemas.UserAuth, Depends(oauth2.get_authenticated_user)],
    skip: int = 0,
    limit: int = 30,
    db: Session = Depends(get_db),
):
    if current_user is None:
        raise HTTPException(status_code=404, detail="User not found")

    return crud.get_dialog(db, user_id=current_user.id, skip=skip, limit=limit)


@router.put(
    "/{dialog_id}", response_model=schemas.DialogGet, status_code=status.HTTP_200_OK
)
def put_dialog(
    current_user: Annotated[schemas.UserAuth, Depends(oauth2.get_authenticated_user)],
    dialog_id=int,
    new_dialog=schemas.DialogEdit,
    db: Session = Depends(get_db),
):
    if current_user is None:
        raise HTTPException(status_code=404, detail="User not found")

    return crud.update_dialog(db, new_dialog, dialog_id=dialog_id)
