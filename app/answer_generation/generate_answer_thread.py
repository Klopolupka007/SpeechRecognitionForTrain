from PyQt5 import QtCore
from data.dialogue_structs import Answer


class GenerateAnswerThread(QtCore.QThread):

    answer_generated = QtCore.pyqtSignal(str, Answer)

    def __init__(self, question_answerer, txt2speech, messages_model, question_text, question_id):
        QtCore.QThread.__init__(self)
        self.question_answerer = question_answerer
        self.txt2speech = txt2speech
        self.messages_model = messages_model
        self.question_text = question_text
        self.question_id = question_id

    def run(self):
        
        answer = self.question_answerer.get_answer(self.question_text)
        audio = self.txt2speech.get_audio(answer)
        inserted_answer = self.messages_model.insert_answer(answer, self.question_id)
        
        self.answer_generated.emit(audio, inserted_answer)