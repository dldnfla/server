from sqlalchemy.orm import Session

from .. import models, oauth2, schemas


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
