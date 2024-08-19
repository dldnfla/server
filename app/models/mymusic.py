from sqlalchemy import Column, Integer, String, ForeignKey

from ..database import Base


class Music(Base):
    __tablename__ = "music"

    id = Column(Integer, primary_key=True, nullable=False, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    singer = Column(String)
    music_title = Column(String)
    music_info = Column(String)
