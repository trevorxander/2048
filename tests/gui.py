from game2048 import gui
from os import sys
from PyQt5 import QtCore, QtWidgets, QtGui




class MainWindow(QtWidgets.QMainWindow):
    def __init__(self):
        QtWidgets.QWidget.__init__(self)
        self.game_area = gui.GameArea(parent=self)
        self.setCentralWidget(self.game_area)

    def keyPressEvent(self, event):
        if event.key() == QtCore.Qt.Key_Left:
            self.game_area.slide_left()
        if event.key() == QtCore.Qt.Key_Right:
            self.game_area.slide_right()
        if event.key() == QtCore.Qt.Key_Up:
            self.game_area.slide_up()
        if event.key() == QtCore.Qt.Key_Down:
            self.game_area.slide_down()
        if event.key() == QtCore.Qt.Key_Space:
            MainWindow.game.undo()



if __name__ == '__main__':

    app = QtWidgets.QApplication(sys.argv)
    w = MainWindow()
    w.show()
    app.processEvents()
    sys.exit(app.exec_())