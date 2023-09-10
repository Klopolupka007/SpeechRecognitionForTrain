from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import DeclarativeBase


class Base(DeclarativeBase):
    pass

class UserCurrentTrain(Base):
    __tablename__ = "user_current_train"
 
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(String)
    train_model = Column(String)