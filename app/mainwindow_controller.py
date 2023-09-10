import datetime
import threading

from playsound import playsound
from PyQt5 import QtCore, QtWidgets
from tzlocal import get_localzone

from answer_generation.generate_answer_thread import GenerateAnswerThread
from answer_generation.question_answerer import QuestionAnswerer
from audio_processing.audio_recorder import AudioRecorder
from audio_processing.voice_recognizer import VoiceRecognizer
from data.messages_model import MessagesModel
from mainwindow import Ui_MainWindow
from message_widgets.answer_widget import Ui_AnswerWidget
from message_widgets.question_widget import Ui_QuestionWidget
from styles.record_button_styles import (RECORD_BUTTON_BASE, RECORD_BUTTON_RECORDING)
from text_to_speech.text_to_speech import TextToSpeech


class MainWindowController:
    def __init__(self, view: Ui_MainWindow):
        self.__view = view
        self.messages_model = MessagesModel()
        self.date_input_format = self.messages_model.DATE_INPUT_FORMAT
        self.DATE_OUTPUT_FORMAT = "%d %B, %H:%M"
        self.micro_button_is_recording = False
        self.__view.micro_button.clicked.connect(self.__micro_button_clicked)
        self.timer = QtCore.QTimer()
        self.elapsed_time = QtCore.QTime(0, 0)
        
        RATE = 16000
        self.MAX_RECORD_SECONDS = 60
        
        self.audio_recorder = AudioRecorder(RATE, self.MAX_RECORD_SECONDS)
        self.voice_recognizer = VoiceRecognizer(RATE)
        
        self.txt2speech = TextToSpeech()
        self.question_answerer = QuestionAnswerer()
        
        self.context = []

    
    def load_conversation(self):
        question_widgets, answer_widgets = self.__get_question_and_answer_widgets()
        for question_widget, answer_widget in zip(question_widgets, answer_widgets):
            self.__view.add_question(question_widget)
            self.__view.add_answer(answer_widget)
        
        q_len, a_len = len(question_widgets), len(answer_widgets)
        min_len = min(q_len, a_len)
        if (q_len < a_len):
            for answer_widget in answer_widgets[min_len:]:
                self.__view.add_answer(answer_widget)
        else:
            for question_widget in question_widgets[min_len:]:
                self.__view.add_question(question_widget)
            
    
    def __micro_button_clicked(self):
        self.micro_button_is_recording = not self.micro_button_is_recording
        self.__view.micro_button.setStyleSheet(RECORD_BUTTON_RECORDING if self.micro_button_is_recording else RECORD_BUTTON_BASE)
        if (self.micro_button_is_recording):
            self.__start_recording()
        else:
            self.__stop_recording()

    
    def __start_recording(self):
        self.timer.start(1000) # in ms
        self.timer.timeout.connect(self.__update_timer)
        
        self.__view.set_timer()
        
        self.micro_read_thread = threading.Thread(target=self.__process_micro)
        self.micro_read_thread.start()


    def __process_micro(self):
        self.frames = self.audio_recorder.start_recording()


    def __update_timer(self):
        self.elapsed_time = self.elapsed_time.addSecs(1)
        self.__view.update_timer(self.elapsed_time.toString("m:ss"))
        if (self.elapsed_time.second() > self.MAX_RECORD_SECONDS):
            self.__micro_button_clicked()
    

    def __stop_recording(self):
        self.audio_recorder.stop_recording()
        
        self.__view.release_timer()
        self.timer.stop()
        self.elapsed_time = QtCore.QTime(0, 0)
        self.timer.timeout.disconnect(self.__update_timer)
        
        self.__view.micro_button.setEnabled(False)
        self.micro_read_thread.join()

        flag = self.__view.checkbox.isChecked()
        print(flag)
        question_text = self.voice_recognizer.recognize_frames(self.frames)
        self.context.append(question_text)
        print(question_text)
        if (question_text):
            inserted_question = self.messages_model.insert_question(question_text)
            
            msg_text = inserted_question.msg_text
            question_sending_time = self.__convert_date_format(inserted_question.sending_datetime)
            
            question_widget = Ui_QuestionWidget()
            question_widget.set_message_content(msg_text, question_sending_time)
            self.__view.add_question(question_widget)
            
            question_id = inserted_question.id
            
            self.generate_answ_thread = GenerateAnswerThread(self.question_answerer, self.context, self.txt2speech, self.messages_model, "я нахожусь в вагоне " + self.__view.combobox.currentText() + ' ' + question_text, question_id)
            self.generate_answ_thread.answer_generated.connect(self.__on_question_answered)
            self.generate_answ_thread.start()
        
        else:
            self.__show_warning()

    
    def __show_warning(self):
        warning_box = QtWidgets.QMessageBox()
        warning_box.setIcon(QtWidgets.QMessageBox.Warning)
        warning_box.setWindowTitle("Внимание")
        warning_box.setText("Не удалось распознать речь.")
        self.__view.micro_button.setEnabled(True)
        warning_box.setStandardButtons(QtWidgets.QMessageBox.Ok)
        warning_box.exec_()


    def __on_question_answered(self, audio, inserted_answer):
        answer_sending_time = self.__convert_date_format(inserted_answer.sending_datetime)
        answer_text = inserted_answer.msg_text
        self.context.append(answer_text)
        answer_widget = Ui_AnswerWidget()
        answer_widget.set_message_content(answer_text, answer_sending_time)
        self.__view.add_answer(answer_widget)
        playsound(audio)
        self.__view.micro_button.setEnabled(True)

    
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
        date = datetime.datetime.strptime(date_str+"+0000", self.date_input_format+"%z")
        
        local_timezone = get_localzone()
        local_datetime = date.astimezone(local_timezone)
        
        date_str = local_datetime.strftime(self.DATE_OUTPUT_FORMAT)
        return date_str