from os import sys
from PyQt5 import QtCore, QtWidgets, QtGui
import game2048
import faulthandler

if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    game = game2048.gui.PlayScreen(parent=None, player_list=['player','AI'], comp_difficulty=1)
    game.show()
    sys.exit(app.exec_())
