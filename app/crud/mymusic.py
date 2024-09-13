from fastapi import HTTPException
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session

from .. import models, oauth2, schemas
import requests

def get_music(db: Session, user_id: int):
    return db.query(models.Music).filter(models.Music.user_id == user_id).first()


def get_my_music(db: Session, user_id: int):
    db_mymusic = db.query(models.Music).filter(models.Music.user_id == user_id).first()

    return db_mymusic


def update_music(db: Session, new_music: schemas.MusicEdit, user_id: int):
    db_music = db.query(models.Music).filter(models.Music.user_id == user_id).first()

    if db_music is None:
        db_music = models.Music(
            user_id=user_id,
            singer="",
            music_title="",
            music_info="",
        )
        db.add(db_music)
        db.commit()
        db.refresh(db_music)

    db.query(models.Music).filter(models.Music.user_id == user_id).update(
        new_music.dict()
    )

    db.commit()

    return get_my_music(db, user_id)

API_KEY = "AIzaSyBL5MLgdM4_o4mdmzhKnDNRwNKpYkfrkAo"

def get_video(db: Session,user_id: int):
    mymusic = get_my_music(db, user_id)

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