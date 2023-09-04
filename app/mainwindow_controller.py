import datetime

from answer_widget import Ui_AnswerWidget
from mainwindow import Ui_MainWindow
from messages_model import MessagesModel
from question_widget import Ui_QuestionWidget


class MainWindowController:
    def __init__(self, view: Ui_MainWindow):
        self.__view = view
        self.messages_model = MessagesModel()
        self.date_input_format = self.messages_model.DATE_INPUT_FORMAT
        self.DATE_OUTPUT_FORMAT = "%d %B, %H:%M"
        #self.__view.runButton.clicked.connect(self.start)

    
    def load_conversation(self):
        question_widgets, answer_widgets = self.__get_question_and_answer_widgets()
        for i in range(len(question_widgets)):
            self.__view.add_question(question_widgets[i])
            self.__view.add_answer(answer_widgets[i])

    
    def __get_question_and_answer_widgets(self):
        questions = self.messages_model.receive_questions()
        answers = self.messages_model.receive_answers()
        
        question_widgets = []
        answer_widgets = []
        
        for question in questions:
            question_widget = Ui_QuestionWidget()
            msg_text = question.msg_text
            sending_datetime = self.__convert_date_format(question.sending_datetime)
            question_widget.set_message_content(msg_text, sending_datetime)
            question_widgets.append(question_widget)
            
        for answer in answers:
            answer_widget = Ui_AnswerWidget()
            msg_text = answer.msg_text
            sending_datetime = self.__convert_date_format(answer.sending_datetime)
            answer_widget.set_message_content(msg_text, sending_datetime)
            answer_widgets.append(answer_widget)
            
        return question_widgets, answer_widgets
            
    
    def __convert_date_format(self, date_str):
        date_str = datetime.datetime.strptime(date_str, self.date_input_format)
        date_str = date_str.strftime(self.DATE_OUTPUT_FORMAT)
        return date_str