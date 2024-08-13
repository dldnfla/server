from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship

from ..database import Base


class Wish(Base):
    __tablename__ = "wish"

    id = Column(Integer, primary_key=True, nullable=False, index=True)
    username = Column(String)
    contents = Column(String)

#쓰레기코드