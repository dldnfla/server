from typing import Annotated

from fastapi import APIRouter, FastAPI, UploadFile, status

app = FastAPI()

router = APIRouter(prefix="/file",tags=["files"])

@router.put("/", status_code=status.HTTP_200_OK)
async def create_upload_file(file: UploadFile):
    return {"filename": file.filename}

