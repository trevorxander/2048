from game2048 import gui
from os import sys
from PyQt5 import QtCore, QtWidgets, QtGui
from threading import Thread
import time
import queue



class MainWindow(QtWidgets.QMainWindow):
    keyboard_buffer = []
    key_pressed = QtCore.pyqtSignal(QtCore.QEvent)
    def __init__(self, parent = None):
        super(QtWidgets.QMainWindow, self).__init__(parent)
        self.game_area = gui.GameArea(parent=self)
        self.setCentralWidget(self.game_area)
        self.resize(self.game_area.size())
        self.event_queue = queue.Queue(maxsize=0)

        self.captured_keys = {QtCore.Qt.Key_Left,
                              QtCore.Qt.Key_Right,
                              QtCore.Qt.Key_Down,
                              QtCore.Qt.Key_Up,
                              QtCore.Qt.Key_Space}

        self.key_pressed.connect(self.game_area.keyPressEvent)

    def keyPressEvent(self, QKeyEvent):
        if QKeyEvent.key() in self.captured_keys:
            QtCore.QCoreApplication.sendEvent(self.game_area,QKeyEvent)

    def process_events(self):
        pass





if __name__ == '__main__':

    app = QtWidgets.QApplication(sys.argv)
    w = MainWindow()
    w.show()
    sys.exit(app.exec_())