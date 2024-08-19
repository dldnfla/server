from sqlalchemy import Column, Integer, String, ForeignKey

from ..database import Base


class Board(Base):
    __tablename__ = "board"

    id = Column(Integer, primary_key=True, nullable=False, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    tag = Column(String)
    title = Column(String)
    contents = Column(String)
    link = Column(String)
    images = Column(String)
