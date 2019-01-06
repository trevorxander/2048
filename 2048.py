from os import sys
import game2048
from PyQt5 import QtCore, QtWidgets, QtGui

if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    game = game2048.gui.TitleScreen()
    sys.exit(app.exec_())