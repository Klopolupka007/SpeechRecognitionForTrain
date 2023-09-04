# -*- coding: utf-8 -*-

from PyQt5 import QtCore, QtWidgets
from base_message_widget import Ui_BaseMessageWidget


class Ui_QuestionWidget(Ui_BaseMessageWidget):
    def __init__(self):
        ALIGNMENT = QtCore.Qt.AlignRight
        COLOR_RGBA = (0, 0, 255, 0.5)
        super().__init__(ALIGNMENT, COLOR_RGBA)