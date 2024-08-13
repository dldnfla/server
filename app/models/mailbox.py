from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship

from ..database import Base


class Mailbox(Base):
    __tablename__ = "mailbox"

    id = Column(Integer, primary_key=True, nullable=False, index=True)
    title = Column(String)
    recipient = Column(String)
    sender = Column(String)
    content = Column(String)
    date = Column(String)