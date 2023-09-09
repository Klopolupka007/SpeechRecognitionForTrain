# -*- coding: utf-8 -*-

from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_BaseMessageWidget(QtWidgets.QWidget):
    def __init__(self, alignment, color):
        if type(self) is Ui_BaseMessageWidget:
            raise TypeError(f"only children of '{Ui_BaseMessageWidget.__name__}' may be instantiated")
        
        super().__init__()
        
        self.__load_elements()
        self.ALIGNMENT = alignment
        self.COLOR_RGBA = color


    def set_message_content(self, text, datetime):
        self.message_text_label.setText(text)
        self.message_sending_datetime.setText(datetime)

        self.verticalLayout.setAlignment(self.ALIGNMENT)
        self.message_sending_datetime.setAlignment(self.ALIGNMENT)
        self.message_text_label.setStyleSheet(f"background-color: qlineargradient(spread:pad, x1:1, y1:0, x2:0, y2:0, stop:0.0646766 rgba{self.COLOR_RGBA[0]}, stop:1 rgba{self.COLOR_RGBA[1]});")


    def __load_elements(self):  
        self.setStyleSheet(
            "background-color: transparent; border-radius: 10px; padding: 10px; margin: 0px; color: white;"
        )
        
        self.verticalLayout = QtWidgets.QVBoxLayout(self)
        self.verticalLayout.setObjectName("verticalLayout")
        
        self.message_text_label = self.__get_message_text_label()
        self.message_text_label.setStyleSheet("color: white;")
        self.verticalLayout.addWidget(self.message_text_label)

        self.message_sending_datetime = self.__get_message_sending_datetime()
        self.verticalLayout.addWidget(self.message_sending_datetime)
        
        self.message_sending_datetime.setStyleSheet(
            "padding: 0px; margin: 0px; color: white;"
        )
    
    
    def __get_message_text_label(self):
        message_text_label_font = QtGui.QFont()
        message_text_label_font.setFamily("Lucida Bright")
        message_text_label_font.setPointSize(12)
        
        message_text_label = QtWidgets.QLabel(self)
        message_text_label.setObjectName("message_text_label")
        message_text_label.setAlignment(QtCore.Qt.AlignLeft|QtCore.Qt.AlignVCenter)
        message_text_label.setWordWrap(True)
        message_text_label.setFont(message_text_label_font)
        
        return message_text_label
    
    
    def __get_message_sending_datetime(self):
        message_sending_datetime_font = QtGui.QFont()
        message_sending_datetime_font.setFamily("Liberation Sans")
        message_sending_datetime_font.setBold(True)
        message_sending_datetime_font.setWeight(75)
        
        message_sending_datetime = QtWidgets.QLabel(self)
        message_sending_datetime.setObjectName("message_sending_datetime")
        message_sending_datetime.setFont(message_sending_datetime_font)
        
        return message_sending_datetime
