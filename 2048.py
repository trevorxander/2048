from os import sys
import game2048
from PyQt5 import QtCore, QtWidgets, QtGui

if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    game = game2048.gui.TitleScreen()
    game.resize(430, 700)
    game.setMinimumSize(game.size())
    sys.exit(app.exec_())