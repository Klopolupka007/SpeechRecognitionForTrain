from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import DeclarativeBase


class Base(DeclarativeBase):
    pass


class Question(Base):
    __tablename__ = "Questions"
 
    id = Column(Integer, primary_key=True, index=True)
    msg_text = Column(String)
    sending_datetime = Column(String)


class Answer(Base):
    __tablename__ = "Answers"
 
    id = Column(Integer, primary_key=True, index=True)
    msg_text = Column(String)
    sending_datetime = Column(String)
    question_id = Column(Integer)