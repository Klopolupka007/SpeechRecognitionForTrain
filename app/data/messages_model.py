from sqlalchemy import create_engine
from sqlalchemy.orm import Session

from data.dialogue_structs import Answer, Question


class MessagesModel:
    def __init__(self):
        self.DATE_INPUT_FORMAT = "%Y-%m-%d %H:%M:%S"
        self.engine = create_engine("sqlite:///data/messages.db")


    def receive_questions(self):
        with Session(autoflush=False, bind=self.engine) as db:
            questions = db.query(Question).all()
            return questions


    def receive_answers(self):
        with Session(autoflush=False, bind=self.engine) as db:
            answers = db.query(Answer).all()
            return answers
        
    
    def insert_question(self, question_text):
        with Session(autoflush=False, bind=self.engine) as db:
            new_question = Question(msg_text=question_text)
            db.add(new_question)
            db.commit()
            inserted_row = db.query(Question).filter_by(id=new_question.id).first()
            return inserted_row
        
        
    def insert_answer(self, answer_text, question_id):
        with Session(autoflush=False, bind=self.engine) as db:
            new_answer = Answer(msg_text=answer_text, question_id=question_id)
            db.add(new_answer)
            db.commit()
            inserted_row = db.query(Answer).filter_by(id=new_answer.id).first()
            return inserted_row


    def __del__(self):
        self.engine.dispose()