from sqlalchemy import create_engine
from sqlalchemy.orm import Session

from data.dialogue_structs import Answer, Question


class MessagesModel:
    def __init__(self):
        self.DATE_INPUT_FORMAT = "%Y-%m-%d %H:%M:%S"
        self.engine = create_engine("sqlite:///data/messages.db", echo=True)


    def receive_questions(self):
        with Session(autoflush=False, bind=self.engine) as db:
            questions = db.query(Question).all()
            return questions


    def receive_answers(self):
        with Session(autoflush=False, bind=self.engine) as db:
            answers = db.query(Answer).all()
            return answers


    def __del__(self):
        self.engine.dispose()