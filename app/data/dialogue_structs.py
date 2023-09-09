from sqlalchemy import Column, Integer, String, text
from sqlalchemy.orm import DeclarativeBase


class Base(DeclarativeBase):
    pass


class Question(Base):
    __tablename__ = "Questions"
 
    id = Column(Integer, primary_key=True, index=True)
    msg_text = Column(String)
    sending_datetime = Column(String, server_default=text("(strftime('%Y-%m-%d %H:%M:%S', 'now'))"))


class Answer(Base):
    __tablename__ = "Answers"
 
    id = Column(Integer, primary_key=True, index=True)
    msg_text = Column(String)
    sending_datetime = Column(String, server_default=text("(strftime('%Y-%m-%d %H:%M:%S', 'now'))"))
    question_id = Column(Integer)