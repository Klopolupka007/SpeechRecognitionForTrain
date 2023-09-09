# -*- coding: utf-8 -*-

from PyQt5 import QtCore

from message_widgets.base_message_widget import Ui_BaseMessageWidget


class Ui_QuestionWidget(Ui_BaseMessageWidget):
    def __init__(self):
        ALIGNMENT = QtCore.Qt.AlignRight
        COLOR_RGBA = ((50, 50, 50, 240), (80, 80, 80, 240))
        super().__init__(ALIGNMENT, COLOR_RGBA)