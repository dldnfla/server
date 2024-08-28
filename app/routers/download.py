from typing import Annotated
import boto3
import uuid
from botocore.exceptions import ClientError
from fastapi import APIRouter, Depends, HTTPException, UploadFile, status

from sqlalchemy.orm import Session

from app.database import get_db

from .. import crud
from app import oauth2, schemas


router = APIRouter(prefix="/download", tags=["file"])


client = boto3.client(
    "s3",
    aws_access_key_id="AKIAXDFC5X3NY5XT3CGH",
    aws_secret_access_key="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",
)

bucket = "ewootz-s3-bucket"

@router.get("/profileimg", status_code=status.HTTP_200_OK)
def download_file(
    current_user: Annotated[schemas.UserAuth, Depends(oauth2.get_authenticated_user)],
    db: Session = Depends(get_db),
):
    user_info = crud.get_user_by_username(db, username=current_user.username)

    profile_image = user_info.profile_image

    return profile_image



@router.get("/postingimg", status_code=status.HTTP_200_OK)
def download_file(
    current_user: Annotated[schemas.UserAuth, Depends(oauth2.get_authenticated_user)],
    db: Session = Depends(get_db),
):
    user_info = crud.get_user_by_username(db, username=current_user.username)

    profile_image = user_info.profile_image

    return profile_image

