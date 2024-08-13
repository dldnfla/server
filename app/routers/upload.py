from typing import Annotated

from fastapi import APIRouter, FastAPI, UploadFile, status, Depends
from sqlalchemy.orm import Session

from app import oauth2

from .. import crud, schemas
from ..database import get_db

app = FastAPI()

router = APIRouter(prefix="/file",tags=["files"])

# @router.put("/", status_code=status.HTTP_200_OK)
# async def create_upload_file(file: UploadFile):
#     return {"filename": file.filename}

@router.put("/", status_code=status.HTTP_200_OK)
def create_upload_file(
    current_user: Annotated[schemas.UserAuth, Depends(oauth2.get_authenticated_user)],
    image: schemas.UserEdit,
    db: Session = Depends(get_db),
):
    if current_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    
    updated_image = schemas.UserEdit(profile_image = image)
    return crud.update_user(db, user_id=current_user.id, new_user = updated_image)

@router.get("/", status_code=status.HTTP_200_OK)
def get_upload_file(
    current_user: Annotated[schemas.UserAuth, Depends(oauth2.get_authenticated_user)],
    skip: int = 0,
    limit: int = 30,
    db: Session = Depends(get_db),
):
    if current_user is None:
        raise HTTPException(status_code=404, detail="User not found")

    return crud.get_user(db, user_id=current_user.id)
