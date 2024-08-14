from typing import Annotated
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app import oauth2

from .. import crud, schemas, models
from ..database import get_db

router = APIRouter(prefix="/follow", tags=["follow"])


@router.post("/", status_code=status.HTTP_201_CREATED)
def create_follow(
    current_user: Annotated[schemas.UserAuth, Depends(oauth2.get_authenticated_user)],
    follow: schemas.FollowCreate,
    db: Session = Depends(get_db),
):
    if follow.follower is None:
        raise HTTPException(status_code=404, detail="User not found")

    follower_get = (
        db.query(models.Follow)
        .filter(
            models.Follow.follower == current_user.id,
            models.Follow.followee == follow.followee,
        )
        .first()
    )

    # 테이블에 매칭이 안되어있는 경우
    if not follower_get:
        return crud.create_follow(db, follow)
    else:  # 테이블에 매칭이 되어있을 경우
        raise HTTPException(status_code=404, detail="Ilchon already exists.")


@router.get("/", status_code=status.HTTP_200_OK)
def get_follow(
    current_user: Annotated[schemas.UserAuth, Depends(oauth2.get_authenticated_user)],
    skip: int = 0,
    limit: int = 30,
    db: Session = Depends(get_db),
):
    if current_user is None:
        raise HTTPException(status_code=404, detail="User not found")

    return crud.get_follow(db, user_id=current_user.id, skip=skip, limit=limit)


@router.put("/", status_code=status.HTTP_200_OK)
def put_follow(
    current_user: Annotated[schemas.UserAuth, Depends(oauth2.get_authenticated_user)],
    follow: schemas.FollowEdit,
    db: Session = Depends(get_db),
):
    follower_get = (
        db.query(models.Follow)
        .filter(
            models.Follow.follower == current_user,
            models.Follow.followee == current_user.username,
        )
        .first()
    )

    # 테이블에 매칭이 되어있는 경우
    if follower_get:
        return crud.update_follow(db, follow, user_id=current_user.id)
    else:  # 테이블에 매칭이 안되어있을 경우
        raise HTTPException(status_code=404, detail="User not found")
