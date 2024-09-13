from typing import Annotated
from fastapi import Depends, HTTPException
from sqlalchemy.orm import Session

from app import crud

from .. import models, schemas


def get_video(db: Session, id: int):
    mymusic = crud.get_my_music(db, id)
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

    ...
