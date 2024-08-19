from typing import Annotated
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app import oauth2

from .. import models, schemas
from ..database import get_db

router = APIRouter(prefix="/search", tags=["search"])


@router.get("/", status_code=status.HTTP_200_OK)
def get_search(
    current_user: Annotated[schemas.UserAuth, Depends(oauth2.get_authenticated_user)],
    search_user: str,
    db: Session = Depends(get_db),
):
    if current_user is None:
        raise HTTPException(status_code=404, detail="User not found")

    result_search = (
        db.query(models.User)
        .filter(models.User.username.ilike(f"{search_user}%"))
        .all()
    )

    return result_search
