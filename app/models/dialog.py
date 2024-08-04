from sqlalchemy import Column, Integer, String

from ..database import Base


class Dialog(Base):
    __tablename__ = "dialog"

    id = Column(Integer, primary_key=True, nullable=False, index=True)
    user_id = Column(String, foreign_key=True)
    visitor = Column(String)
    contents = Column(String)
