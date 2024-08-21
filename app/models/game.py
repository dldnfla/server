from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship

from ..database import Base


class Mailbox(Base):
    __tablename__ = "score"
    
    id = Column(Integer, primary_key=True, nullable=False, index=True)
    username = Column(String, ForeignKey("users.username"), nullable=False)
    score = Column(Integer, nullable=False)
