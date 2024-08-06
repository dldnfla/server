from typing import Annotated
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app import oauth2

from .. import crud, schemas
from ..database import get_db

router = APIRouter(prefix="/dialog", tags=["dialog"])


@router.post("/", status_code=status.HTTP_201_CREATED)
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
     
    return crud.get_dialog(db, skip=skip, limit=limit)


@router.put("/{dialog_id}", status_code=status.HTTP_200_OK)
def put_dialog(
    current_user: Annotated[schemas.UserAuth, Depends(oauth2.get_authenticated_user)],
    dialog_id = int,  # 도대체 어케 받아오는지 모르겟음(약간 저능)
    dialog = schemas.DialogCreate,
    db: Session = Depends(get_db),
):
    if current_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    
    return crud.update_dialog(db, dialog_id, dialog)

    # client가 dialog id를 보내주려면 처음에 dialog를 만들때 response로 보내줘야됨 -> 스키마 수정
    # 왜 이 스키마가 필요한지 생각해보면 일단
    # 1. DialogBase -> 필수 속성 모음
    # 2. DialogCreate -> dialog 하나 만들때 필수 속성 다 필요함
    # 3. 근데 지금 필요한 건 dialog 하나의 아이디를 포함한 스키마
    # 4. 그럼 DialogGet이라는 스키마를 하나 더 만든다.
    # 5. 그리고 dialog post 할 때 response_model로 DialogGet을 주면 됨
    # 6. model에서 primary key 설정하면 autoincrement 돼서 값 줄 필요 X
    # 7. 스키마 = 프론트랑 소통할 때 필요한 거
    # 8. model, schema, crud init 파일에 from .파일이름 import * 필수 
    # 9. 로그인한 유저만 사용 가능한 기능이면 추가한 코드 current_user 처럼 하면 로그인한 유저만 사용가능 
    # 10. 방명록은 다는 사람은 로그인 안해도 돼서 current_user 사용 X 
    # 띄어쓰기 ㅂㅌ합니다
