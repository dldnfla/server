from typing import Annotated
from fastapi import FastAPI, HTTPException, APIRouter, status, Depends
from fastapi.responses import JSONResponse
import requests
import urllib.parse

from .. import schemas
from app import oauth2

app = FastAPI()

router = APIRouter(prefix="/youtube", tags=["youtube"])

API_KEY = "AIzaSyBL5MLgdM4_o4mdmzhKnDNRwNKpYkfrkAo"

@router.post("/", status_code=status.HTTP_200_OK)
async def keyword_search_data(
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
            "part": "snippet", #id, snippet 있는데 대부분의 정보가 snippet에 잇음ㅁ
            "type": "video", #채널, 플레이리스트, 영상 등 받아올 정보 타입?
            "maxResults": 10, #개수
            "videoEmbeddable": "true", #퍼가기 가능한 영상만 가지고 오기
            "fields": "items(id, snippet)",
            "q": urllib.parse.quote(search) #검색어
        }

        # GET 요청을 보내고 응답을 받음
        response = requests.get(api_url, params=params)
        response.raise_for_status()  # 요청이 실패하면 예외 발생

        # JSON 응답 반환
        return JSONResponse(content=response.json())
    
    except requests.exceptions.RequestException as e:
        print("예외상황 발생:", str(e))
        raise HTTPException(status_code=500, detail="YouTube API 요청 중 오류 발생")

