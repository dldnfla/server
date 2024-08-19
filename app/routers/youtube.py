from typing import Annotated
from fastapi import FastAPI, HTTPException, APIRouter, status, Depends
from fastapi.responses import JSONResponse
import requests
from sqlalchemy.orm import Session

from .. import schemas, crud
from app import oauth2

from ..database import get_db

app = FastAPI()

router = APIRouter(prefix="/youtube", tags=["youtube"])


API_KEY = "AIzaSyBL5MLgdM4_o4mdmzhKnDNRwNKpYkfrkAo"


@router.post("/mymusic", status_code=status.HTTP_201_CREATED)
def create_my_music(
    current_user: Annotated[schemas.UserAuth, Depends(oauth2.get_authenticated_user)],
    music: schemas.MusicCreate,
    db: Session = Depends(get_db),
):
    if current_user is None:
        raise HTTPException(status_code=404, detail="User not found")

    return crud.create_music(db, music, user_id=current_user.id)


@router.get("/search", status_code=status.HTTP_200_OK)
async def search_vidieo(
    search: str,
    current_user: Annotated[schemas.UserAuth, Depends(oauth2.get_authenticated_user)],
):
    if current_user is None:
        raise HTTPException(status_code=404, detail="User not found")

    try:
        # YouTube API 기본 URL
        api_url = "https://www.googleapis.com/youtube/v3/search"

        # API 요청에 필요한 파라미터
        params = {
            "key": API_KEY,
            "part": "snippet",  # id, snippet 있는데 대부분의 정보가 snippet에 잇음ㅁ
            "type": "video",  # 채널, 플레이리스트, 영상 등 받아올 정보 타입?
            "maxResults": 2,  # 개수
            "videoEmbeddable": "true",  # 퍼가기 가능한 영상만 가지고 오기
            "fields": "items(id, snippet)",
            "q": search,  # 검색어
        }

        # GET 요청을 보내고 응답을 받음
        response = requests.get(api_url, params=params)
        response.raise_for_status()  # 요청이 실패하면 예외 발생

        # JSON 응답 반환
        return JSONResponse(content=response.json())

    except requests.exceptions.RequestException as e:
        print("예외상황 발생:", str(e))
        raise HTTPException(status_code=500, detail="YouTube API 요청 중 오류 발생")


@router.get("/mymusic_video", status_code=status.HTTP_200_OK)
def get_video(
    current_user: Annotated[schemas.UserAuth, Depends(oauth2.get_authenticated_user)],
    db: Session = Depends(get_db),
):
    if current_user is None:
        raise HTTPException(status_code=404, detail="User not found")

    mymusic = crud.get_my_music(db, current_user.id)

    try:
        # YouTube API videos 엔드포인트 URL
        api_url = "https://www.googleapis.com/youtube/v3/videos"

        # API 요청에 필요한 파라미터
        params = {
            "key": API_KEY,
            "part": "snippet,contentDetails,statistics",  # 원하는 비디오의 정보 유형
            "id": mymusic.music_info,
            "fields": "items(id,snippet,contentDetails,statistics)",  # 필요한 필드만 선택
        }

        response = requests.get(api_url, params=params)
        response.raise_for_status()

        youtube_data = response.json()

        custom_response = {
            "youtube_data": youtube_data,
            "singer": mymusic.singer,
            "music_title": mymusic.music_title,
        }

        return JSONResponse(content=custom_response)

    except requests.exceptions.RequestException as e:
        print("예외상황 발생:", str(e))
        raise HTTPException(status_code=500, detail="YouTube API 요청 중 오류 발생")
