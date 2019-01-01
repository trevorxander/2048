from PyQt5 import QtCore, QtGui, QtWidgets, uic
from game2048 import gui

class GameGrid (QtWidgets.QWidget):
    def __init__(self, parent = None, matrix = None):
        QtWidgets.QWidget.__init__(self, parent = parent)
        ui = uic.loadUi('../game2048/gui/play_screen/game/game_grid.ui', self)

        self._old_matrix = matrix
        self.grid = ui.grid_frame
        grid: QtWidgets.QFrame

        self.grid_size = len(matrix)
        self.gui_matrix = []
        self.initialize_grid(matrix)


        corner_tile = self.gui_matrix[self.grid_size - 1][self.grid_size - 1]
        frame_thickness = 11
        width = corner_tile.location[0] + corner_tile.width() + frame_thickness* 2
        height = corner_tile.location[1] + corner_tile.height() + frame_thickness * 2
        self.setMinimumWidth(width)
        self.setMinimumHeight(height)


        self.show()


    def initialize_grid(self, game_matrix):
        for row in range(self.grid_size):
            tile_row = []
            for col in range(self.grid_size):
                new_tile = gui.Tile(parent=self.grid, value=game_matrix[row][col], pos=(row, col))
                tile_row.append(new_tile)
            self.gui_matrix.append(tile_row)

    def update_grid(self, new_matrix):
        for row in range(len(new_matrix)):
            for col in range(len(new_matrix)):
                self.gui_matrix[row][col].value = new_matrix [row][col]

    def resizeEvent(self, QResizeEvent):
        QResizeEvent: QtGui.QResizeEvent
        size: QtCore.QSize

        for row in self.gui_matrix:
            for tile in row:
                pass
                #tile._map_from_pos()
