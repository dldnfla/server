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
    # if follow.follower is None:
    #     raise HTTPException(status_code=404, detail="User not found")
    # 이렇게 처리하면 그냥 입력 안하면 User not found 로 처리돼서 내가 crud에 처리한 거처럼 처리해야돼
    # 디비에 접근하는 건 다 crud로 분리가 규칙

    follower_get = crud.check_follow_request(
        db, follower=current_user.username, followee=follow.followee
    )
    # 여기 . user.id 로 처리 했던데 스키마를 str로 했으면 current_user도 str
    # 테이블에 매칭이 안되어있는 경우
    if not follower_get:
        return crud.create_follow(db, follow)
    else:  # 테이블에 매칭이 되어있을 경우
        raise HTTPException(status_code=404, detail="Follow suggestion already sended")


@router.get("/", status_code=status.HTTP_200_OK)
def get_follow(
    current_user: Annotated[schemas.UserAuth, Depends(oauth2.get_authenticated_user)],
    skip: int = 0,
    limit: int = 30,
    db: Session = Depends(get_db),
):
    if current_user is None:
        raise HTTPException(status_code=404, detail="User not found")

    return crud.get_follow(db, username=current_user.username, skip=skip, limit=limit)


"""
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
        )
        .first()
    )

    # 스키마를 int 로 짰는지 str로 짰는지 확인 할 것 
    # int 로 짯으면 user_id 로 매개변수 이름 통일하고 str로 짰으면 username으로 

    # 테이블에 매칭이 되어있는 경우
    if follower_get:
        return crud.update_follow(db, follow, username=current_user.username)
    else:  # 테이블에 매칭이 안되어있을 경우
        raise HTTPException(status_code=404, detail="User not found")
"""
