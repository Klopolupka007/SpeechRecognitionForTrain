from sqlalchemy import create_engine
from sqlalchemy.orm import Session

from user_train_struct import UserCurrentTrain


class UsersTrainDataModel:
    def __init__(self):
        self.DATE_INPUT_FORMAT = "%Y-%m-%d %H:%M:%S"
        self.engine = create_engine("sqlite:///telegram_version/database/userdata.db")

    def get_current_train_of_user(self, user_id: str)->str:
        with Session(autoflush=False, bind=self.engine) as db:
            train_model = db.query(UserCurrentTrain).filter_by(user_id=user_id).first()
            return train_model.train_model
        
    def is_user_exists(self, user_id: str)->bool:
        with Session(autoflush=False, bind=self.engine) as db:
            train_model = db.query(UserCurrentTrain).filter_by(user_id=user_id).first()
            return train_model is not None
        
    def insert_train(self, user_id: str, train_model: str)->UserCurrentTrain:
        if (self.is_user_exists(user_id)):
            with Session(autoflush=False, bind=self.engine) as db:
                db.query(UserCurrentTrain).filter_by(user_id=user_id).update({"train_model":train_model})
                db.commit()
                inserted_row = db.query(UserCurrentTrain).filter_by(user_id=user_id).first()
        else:
            with Session(autoflush=False, bind=self.engine) as db:
                new_user_train = UserCurrentTrain(user_id=user_id, train_model=train_model)
                db.add(new_user_train)
                db.commit()
                inserted_row = db.query(UserCurrentTrain).filter_by(id=new_user_train.id).first()
        
        return inserted_row


    def __del__(self):
        self.engine.dispose()
        