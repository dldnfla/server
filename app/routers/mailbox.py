from typing import Annotated
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app import oauth2

from .. import crud, schemas
from ..database import get_db

router = APIRouter(prefix="/mailbox", tags=["mailbox"])


@router.post("/", status_code=status.HTTP_201_CREATED)
def create_mailbox(
    current_user: Annotated[schemas.UserAuth, Depends(oauth2.get_authenticated_user)],
    mailbox: schemas.MailboxCreate,
    db: Session = Depends(get_db),
):
    if current_user is None:
        raise HTTPException(status_code=404, detail="User not found")

    return crud.create_dialog(db, mailbox)