from sqlalchemy import Column, Integer, String
#from sqlalchemy.orm import relationship

from ..database import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, nullable=False, index=True)
    user_id = Column(String,primary_key = True, nullable=False)
    user_password = Column(String, nullable=False)
    username = Column(String)
    status_message = Column(String)
    user_url = Column(String, nullable=False)
    music_info = Column(String)


