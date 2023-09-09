# -*- coding: utf-8 -*-

from PyQt5 import QtCore, QtGui, QtWidgets

from message_widgets.answer_widget import Ui_AnswerWidget
from message_widgets.question_widget import Ui_QuestionWidget
from styles.record_button_styles import RECORD_BUTTON_BASE


class Ui_MainWindow(QtWidgets.QMainWindow):

    def __init__(self):
        super().__init__()

        # Window settings
        self.setObjectName("MainWindow")
        self.setWindowTitle("Помощник машиниста")
        self.setMinimumSize(500, 700)
        
        self.setStyleSheet("QMainWindow#MainWindow{background-color: rgba(30,30,30, 1);}")
        
        self.central_widget = QtWidgets.QWidget(self)
        self.central_widget.setObjectName("centralwidget")
        
        # Set up Main layout
        self.central_layout = QtWidgets.QVBoxLayout(self.central_widget)
        self.central_layout.setObjectName("vBoxLayout")
        
        self.__get_scroll_area()
        
        # Add micro button
        self.micro_button = self.__get_micro_button()
        self.central_layout.addWidget(self.micro_button)
        self.central_layout.setAlignment(self.micro_button, QtCore.Qt.AlignCenter)
        
        self.timer_label = self.__get_timer_label()
        self.central_layout.addWidget(self.timer_label)
        
        self.setCentralWidget(self.central_widget)
        

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
        
    
    def set_timer(self):
        self.timer_label.setVisible(True)
        
    def update_timer(self, time):
        self.timer_label.setText(time)

    def release_timer(self):
        self.timer_label.setText("")
        self.timer_label.setVisible(False)
        

    def __get_micro_button(self):
        micro_button = QtWidgets.QPushButton(self.central_widget)
        micro_button.setObjectName("micro_button")
        micro_button.setText("")
        micro_button.setStyleSheet(RECORD_BUTTON_BASE)
        return micro_button


    def __get_scroll_area(self):
        self.scroll_area = QtWidgets.QScrollArea(self.central_widget)
        self.scroll_area.setObjectName("scroll_area")
        self.scroll_area.setWidgetResizable(True)
        self.scroll_area.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.scroll_area.setStyleSheet("QScrollArea#scroll_area { background-color:transparent; background-image: transparent; border: 2px solid rgb(50,50,50);};")

        # Create a widget to contain the message widgets
        message_container = QtWidgets.QWidget(self.scroll_area)
        message_container.setObjectName("message_container")
        message_container.setStyleSheet("QWidget#message_container {background-color:transparent;}")
        self.scroll_area.setWidget(message_container)
        self.scroll_area.verticalScrollBar().rangeChanged.connect(self.scroll_to_bottom)

        # Create a QVBoxLayout for the message container
        self.messages_vertical_layout = QtWidgets.QVBoxLayout()

        # Set the message layout for the message container
        message_container.setLayout(self.messages_vertical_layout)

        # Add the scroll area to the central layout
        self.central_layout.addWidget(self.scroll_area)
        
        self.statusBar().setStyleSheet("background-color: transparent;")
    
    
    def __get_timer_label(self):
        timer_label = QtWidgets.QLabel()
        timer_label.setVisible(False)
        timer_label.setAlignment(QtCore.Qt.AlignHCenter|QtCore.Qt.AlignVCenter)
        timer_label.setWordWrap(True)
        timer_label.setStyleSheet("color: white;")
        
        timer_label_font = QtGui.QFont()
        timer_label_font.setFamily("Consolas")
        timer_label_font.setPointSize(14)
        
        timer_label.setFont(timer_label_font)
        
        return timer_label


from resources import resources
