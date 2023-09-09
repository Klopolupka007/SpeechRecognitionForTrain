# -*- coding: utf-8 -*-

from PyQt5 import QtCore

from message_widgets.base_message_widget import Ui_BaseMessageWidget


class Ui_AnswerWidget(Ui_BaseMessageWidget):
    def __init__(self):
        ALIGNMENT = QtCore.Qt.AlignLeft
        COLOR_RGBA = ((30, 70, 110, 240), (30, 70, 190, 240))
        super().__init__(ALIGNMENT, COLOR_RGBA)        