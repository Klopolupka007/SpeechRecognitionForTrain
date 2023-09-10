from sqlalchemy import create_engine
from sqlalchemy.orm import Session

from user_dialogue_struct import UserDialogue


class UsersDialogueModel:
    def __init__(self):
        self.DATE_INPUT_FORMAT = "%Y-%m-%d %H:%M:%S"
        self.engine = create_engine("sqlite:///telegram_version/database/userdata.db")

    def get_dialogue(self, user_id: str):
        with Session(autoflush=False, bind=self.engine) as db:
            dialogue = db.query(UserDialogue).filter_by(user_id=user_id).all()
            return dialogue
        
    
    def clear_dialogue(self, user_id: str):
        with Session(autoflush=False, bind=self.engine) as db:
            db.query(UserDialogue).filter_by(user_id=user_id).delete()
            db.commit()
    
            
    def insert_qa(self, user_id: str, question: str, answer: str)->UserDialogue:
        with Session(autoflush=False, bind=self.engine) as db:
            new_qa = UserDialogue(user_id=user_id, question=question, answer=answer)
            db.add(new_qa)
            db.commit()
            inserted_row = db.query(UserDialogue).filter_by(id=new_qa.id).first()
    
        return inserted_row


    def __del__(self):
        self.engine.dispose()
        
        
#UsersDialogueModel().insert_train("775618173", "Вопрос", "Ответ")
#UsersDialogueModel().insert_train("775618173", "Вопрос2", "Ответ2")
#UsersDialogueModel().clear_dialogue("775618173")
