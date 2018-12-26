from game.model import Game2048
from os import sys
from PyQt5 import QtCore, QtGui, QtWidgets



class MainWindow(QtWidgets.QMainWindow):
    game = Game2048(4)
    testno = 0
    def __init__(self):
        QtWidgets.QMainWindow.__init__(self)
        MainWindow.game._print()


    def keyPressEvent(self, event):

        if event.key() == QtCore.Qt.Key_Left:
            MainWindow.game.left()
        if event.key() == QtCore.Qt.Key_Right:
            MainWindow.game.right()
        if event.key() == QtCore.Qt.Key_Up:
            MainWindow.game.up()
        if event.key() == QtCore.Qt.Key_Down:
            MainWindow.game.down()
        if event.key() == QtCore.Qt.Key_Space:
            MainWindow.game._rand_pop_in()
        MainWindow.game._print()





if __name__ == '__main__':

    app = QtWidgets.QApplication(sys.argv)
    w = MainWindow()
    w.show()
    app.processEvents()
    sys.exit(app.exec_())