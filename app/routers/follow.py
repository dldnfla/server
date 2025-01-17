from typing import Annotated
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app import oauth2

from .. import crud, schemas, models
from ..database import get_db

router = APIRouter(prefix="/api/follow", tags=["follow"])


@router.post("/", status_code=status.HTTP_201_CREATED)
def create_follow(
    current_user: Annotated[schemas.UserAuth, Depends(oauth2.get_authenticated_user)],
    follow: schemas.FollowCreate,
    db: Session = Depends(get_db),
):
    followee_get = crud.check_follow_request(
        db, follower=current_user.username, followee=follow.followee
    )

    if followee_get:
        raise HTTPException(status_code=404, detail="you already requested")

    else:  # 테이블에 매칭이 안돼있는 경우
        return crud.create_follow(db, follow)


@router.get("/", status_code=status.HTTP_200_OK)
def get_follower(
    current_user: Annotated[schemas.UserAuth, Depends(oauth2.get_authenticated_user)],
    db: Session = Depends(get_db),
):
    if current_user is None:
        raise HTTPException(status_code=404, detail="User not found")

    return crud.get_follow(db, username=current_user.username)


@router.get("/requests", status_code=status.HTTP_200_OK)
def get_follow_request(
    current_user: Annotated[schemas.UserAuth, Depends(oauth2.get_authenticated_user)],
    db: Session = Depends(get_db),
):
    if current_user is None:
        raise HTTPException(status_code=404, detail="User not found")

    return crud.get_follow_request(db, username=current_user.username)


@router.put("/", status_code=status.HTTP_200_OK)
def put_follow(
    current_user: Annotated[schemas.UserAuth, Depends(oauth2.get_authenticated_user)],
    follow: schemas.FollowEdit,
    db: Session = Depends(get_db),
):
    follower_get = (
        db.query(models.Follow)
        .filter(
            models.Follow.follower == follow.follower,
            models.Follow.followee == current_user.username,
            models.Follow.follow_get == False,
        )
        .first()
    )

    # 테이블에 매칭이 되어있는 경우
    if follower_get:
        return crud.update_follow(db, follow, username=current_user.username)
    else:  # 테이블에 매칭이 안되어있을 경우
        raise HTTPException(status_code=404, detail="User not found")
