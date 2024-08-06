from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from .. import crud, schemas
from ..database import get_db

router = APIRouter(prefix="/dialog", tags=["dialog"])


@router.post("/", status_code=status.HTTP_201_CREATED)
def create_dialog(
    dialog: schemas.DialogCreate,
    db: Session = Depends(get_db),
):
    return crud.create_dialog(db, dialog)


@router.get("/", status_code=status.HTTP_200_OK)
def get_dialog(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
):
    return crud.get_dialog(db, skip=skip, limit=limit)


@router.put("/{dialog_id}", status_code=status.HTTP_200_OK)
def put_dialog(
    dialog_id=int,  # 도대체 어케 받아오는지 모르겟음(약간 저능)
    dialog=schemas.DialogCreate,
    db: Session = Depends(get_db),
):
    return crud.update_dialog(db, dialog_id, dialog)
