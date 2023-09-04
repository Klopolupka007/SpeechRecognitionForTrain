# -*- coding: utf-8 -*-

from PyQt5 import QtCore, QtWidgets
from answer_widget import Ui_AnswerWidget
from question_widget import Ui_QuestionWidget


class Ui_MainWindow(QtWidgets.QMainWindow):

    def __init__(self):
        super().__init__()

        # Window settings
        self.setObjectName("MainWindow")
        self.setWindowTitle("Умник хренов")
        self.resize(700, 600)
        
        self.centralwidget = QtWidgets.QWidget(self)
        self.centralwidget.setObjectName("centralwidget")
        
        # Set up Main layout
        self.mainLayout = QtWidgets.QVBoxLayout(self.centralwidget)
        self.mainLayout.setObjectName("vBoxLayout")
        
        # Add micro button
        self.micro_button = self.__get_micro_button()
        self.mainLayout.addWidget(self.micro_button)
        self.mainLayout.setAlignment(self.micro_button, QtCore.Qt.AlignCenter)
        
        # Messages vertical layout
        chat_frame = QtWidgets.QFrame()
        self.messages_vertical_layout = self.__get_messages_vertical_layout(chat_frame)

        # Create a Scroll Area
        self.scroll_area = self.__get_scroll_area(chat_frame)
        self.mainLayout.addWidget(self.scroll_area)
        
        self.setCentralWidget(self.centralwidget)
        

    def add_question(self, question_widget: Ui_QuestionWidget):
        question_widget.setSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Fixed)
        self.messages_vertical_layout.setAlignment(question_widget, QtCore.Qt.AlignLeft)
        self.messages_vertical_layout.addWidget(question_widget)
        

    def add_answer(self, answer_widget: Ui_AnswerWidget):
        answer_widget.setSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Fixed)
        self.messages_vertical_layout.setAlignment(answer_widget, QtCore.Qt.AlignRight)
        self.messages_vertical_layout.addWidget(answer_widget)


    def scroll_to_bottom(self):
        self.scroll_area.verticalScrollBar().setValue(self.scroll_area.verticalScrollBar().maximum())
        

    def __get_micro_button(self):
        micro_button = QtWidgets.QPushButton(self.centralwidget)
        micro_button.setObjectName("micro_button")
        micro_button.setText("")
        micro_button.setStyleSheet(
            """
            QPushButton {
                background-color: white;
                border-style: solid;
                border-width:1px;
                border-color: black;
                border-radius:50px;
                max-width:100px;
                max-height:100px;
                min-width:100px;
                min-height:100px;
                image: url(:/images/micro.png);
            }
            QPushButton:hover {
                border-width:2px;
            }
            QPushButton:pressed {
                background-color: rgb(200,200,200);
                border-width:3px;
            }
            """
        )
        return micro_button
    

    def __get_messages_vertical_layout(self, chat_frame):
        messages_vertical_layout = QtWidgets.QVBoxLayout(chat_frame)
        messages_vertical_layout.setObjectName("messages_vertical_layout")
        messages_vertical_layout.setAlignment(QtCore.Qt.AlignBottom)
        return messages_vertical_layout


    def __get_scroll_area(self, chat_frame):
        scroll_area = QtWidgets.QScrollArea(self.centralwidget)
        scroll_area.setWidget(chat_frame)
        scroll_area.setWidgetResizable(True)
        return scroll_area


from resources import resources