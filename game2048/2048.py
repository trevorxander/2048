#!/usr/bin/env python3
import sys

from PyQt5 import QtWidgets

import game2048


def run_game():
    app = QtWidgets.QApplication(sys.argv)
    game = game2048.gui.TitleScreen()
    game.resize(430, 700)
    game.setMinimumSize(game.size())
    sys.exit(app.exec_())


if __name__ == '__main__':
    run_game()
