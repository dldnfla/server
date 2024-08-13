from sqlalchemy import Column, Integer, String, ForeignKey, Boolean
from sqlalchemy.orm import relationship

from ..database import Base


class Follow(Base):
    __tablename__ = "follow"

    id = Column(Integer, primary_key=True, nullable=False, index=True)
    follower = Column(String, ForeignKey("users.id"), nullable=False)
    followee = Column(String, ForeignKey("users.id"), nullable=False)
    follow_get = Column(Boolean, nullable=False)
