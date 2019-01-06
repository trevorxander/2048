from os import sys
from PyQt5 import QtCore, QtWidgets, QtGui
import game2048

if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    game = game2048.gui.TitleScreen()
    sys.exit(app.exec_())