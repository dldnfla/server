from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship

from ..database import Base


class Qna(Base):
    __tablename__ = "qna"

    id = Column(Integer, primary_key=True, nullable=False, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    answer1 = Column(String)
    answer2 = Column(String)
    answer3 = Column(String)
    answer4 = Column(String)
    answer5 = Column(String)
    answer6 = Column(String)
    answer7 = Column(String)
    answer8 = Column(String)
    answer9 = Column(String)
    answer10 = Column(String)
