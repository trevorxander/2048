from PyQt5 import QtCore, QtGui, QtWidgets, uic
import game2048
from game2048 import gui

class GameArea (QtWidgets.QWidget):

    def __init__(self, parent = None, label='2048', game_size=4, has_undo = True):
        QtWidgets.QWidget.__init__(self, parent = parent)
        self.ui = uic.loadUi('../game2048/gui/play_screen/game_area.ui', self)
        self.game_model = game2048.Model2048 (matrix_size=game_size)

        game_box = self.ui.game_grid_box
        game_box: QtWidgets.QHBoxLayout

        self.game_grid = gui.GameGrid(matrix=self.game_model.get_matrix())
        game_box.addWidget(self.game_grid)
        self.show()

    def slide_left(self):
        self.game_model.left()
        self.update_game()

    def slide_right(self):
        self.game_model.right()
        self.update_game()

    def slide_down(self):
        self.game_model.down()
        self.update_game()

    def slide_up(self):
        self.game_model.up()
        self.update_game()

    def update_game(self):
        self.game_grid.update_grid(self.game_model.get_matrix())
        self.game_model._print()
        # moved_tiles = self.game_model.get_moved_tiles()
        # for movement in moved_tiles:
        #     old_tile = movement[0]
        #     new_tile = moved_tiles[1]
        #     self.game_grid.animate(old_tile, new_tile)

