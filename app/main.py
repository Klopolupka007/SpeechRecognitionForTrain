import sys
from PyQt5 import QtWidgets

from mainwindow import Ui_MainWindow
from mainwindow_controller import MainWindowController


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    ui = Ui_MainWindow()
    
    mainwindow_controller = MainWindowController(ui)
    mainwindow_controller.load_conversation()

    ui.show()
    ui.scroll_to_bottom()

    sys.exit(app.exec_())