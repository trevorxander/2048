from game2048 import gui
from os import sys
from PyQt5 import QtCore, QtWidgets, QtGui
import time



class MainWindow(QtWidgets.QMainWindow):
    event_processing = False
    def __init__(self):
        QtWidgets.QWidget.__init__(self)
        self.game_area = gui.GameArea(parent=self)
        self.setCentralWidget(self.game_area)
        self.input_buffer = []
        self.resize(self.game_area.size())


    def keyPressEvent(self, event):
        time_start = time.time()
        self.input_buffer.append(event.key())
        if event.key() == QtCore.Qt.Key_Left:
            self.game_area.slide_left()
        elif event.key() == QtCore.Qt.Key_Right:
            self.game_area.slide_right()
        elif event.key() == QtCore.Qt.Key_Up:
            self.game_area.slide_up()
        elif event.key() == QtCore.Qt.Key_Down:
            self.game_area.slide_down()
        elif event.key() == QtCore.Qt.Key_Space:
            self.game_area.undo_last_move()
        time_end = time.time()
        print(time_end - time_start)



if __name__ == '__main__':

    app = QtWidgets.QApplication(sys.argv)
    w = MainWindow()
    w.show()
    app.processEvents()
    sys.exit(app.exec_())