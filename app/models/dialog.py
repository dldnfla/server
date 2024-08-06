from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship

from ..database import Base


class Dialog(Base):
    __tablename__ = "dialog"

    id = Column(Integer, primary_key=True, nullable=False, index=True)
    user_id = Column(String, ForeignKey("users.id"), nullable=False)
    # 외래키 설정할 때 "" 안에는 테이블.속성명 이라서 users.id 로 수정
    # 이런 식으로 유저 정보가 필요한 건 지금 니 코드엔 없으니까 신경 ㄴㄴ
    visitor = Column(String)
    contents = Column(String)
