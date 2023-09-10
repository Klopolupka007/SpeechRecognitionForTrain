from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import DeclarativeBase


class Base(DeclarativeBase):
    pass

class UserDialogue(Base):
    __tablename__ = "dialogues"
 
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(String)
    question = Column(String)
    answer = Column(String)