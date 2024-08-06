from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship

from ..database import Base


class Dialog(Base):
    __tablename__ = "dialog"

    id = Column(Integer, primary_key=True, nullable=False, index=True)
    user_id = Column(String, ForeignKey("user_id"), nullable=False)
    visitor = Column(String)
    contents = Column(String)

    user = relationship("User", back_populates="dialogs")
