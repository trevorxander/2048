from PyQt5 import QtCore, QtGui, QtWidgets, uic
from game2048 import gui


class GameGrid(QtWidgets.QWidget):
    MARGIN_SIZE = 12
    DEFAULT_ANIMATION_DURATION = 100
    DEFAULT_STYLE = 'QFrame {{background-color: {color};' \
                    'border: 1px solid {color};' \
                    'border-radius: 10px;}}'
    GRID_COLOR = 'rgb(185,173,162)'

    def __init__(self, parent=None, matrix=None):
        QtWidgets.QWidget.__init__(self, parent=parent)

        ui = GameGridUI()
        ui.setupUi(self)
        self.animation_duration = self.DEFAULT_ANIMATION_DURATION

        self.game_matrix = matrix
        self.grid = ui.grid_frame
        self.tile_length = 150
        self.grid_size = len(matrix)
        self.gui_matrix = []
        self.tile_to_delete = []
        self.initialize_grid()

        self.corner_tile = self.gui_matrix[self.grid_size - 1][self.grid_size - 1]
        self.frame_thickness = 10

        self.animations = QtCore.QParallelAnimationGroup()

        self.setStyleSheet(self.DEFAULT_STYLE.format(color=self.GRID_COLOR))

        self.setMinimumWidth(103.75 * self.grid_size + self.MARGIN_SIZE * 2)
        self.setMinimumHeight(104.75 * self.grid_size + self.MARGIN_SIZE * 2)

        self.setMaximumWidth(103.75 * 1.5 * self.grid_size + self.MARGIN_SIZE * 2)
        self.setMaximumHeight(100.75 * 1.5 * self.grid_size + self.MARGIN_SIZE * 2)

        self.resize(self.minimumWidth(), self.minimumHeight())

        self.show()

    def initialize_grid(self):
        for row in range(self.grid_size):
            tile_row = []
            for col in range(self.grid_size):
                new_tile = gui.Tile(parent=self.grid, value=self.game_matrix[row][col], pos=(row, col))
                new_tile.length = self.tile_length
                tile_row.append(new_tile)
            self.gui_matrix.append(tile_row)

    def update_grid(self, new_matrix):
        for row in range(len(new_matrix)):
            for col in range(len(new_matrix)):
                if self.gui_matrix[row][col].value != new_matrix[row][col]:
                    self.gui_matrix[row][col].value = new_matrix[row][col]

    def get_tile(self, row, col):
        return self.gui_matrix[row][col]

    def animate_tile(self, tile_current_pos, tile_final_pos, value):
        source_tile = self.gui_matrix[tile_current_pos[0]][tile_current_pos[1]]
        destination_tile = self.gui_matrix[tile_final_pos[0]][tile_final_pos[1]]
        moving_tile = gui.Tile(parent=self.grid, pos=tile_current_pos, value=source_tile.value)
        moving_tile.length = self.tile_length

        init_loc = source_tile.geometry()
        final_loc = destination_tile.geometry()

        merge_animation = None
        if source_tile.value == destination_tile.value:
            merge_animation = self.animate_tile_wobble(destination_tile)

        source_tile.value = 0

        tile_movement = QtCore.QPropertyAnimation(moving_tile, b"geometry")
        tile_movement.setDuration(self.animation_duration)
        tile_movement.setStartValue(init_loc)
        tile_movement.setEndValue(final_loc)

        move_and_merge = QtCore.QSequentialAnimationGroup()
        move_and_merge.addAnimation(tile_movement)
        if merge_animation is not None:
            move_and_merge.addAnimation(merge_animation)

        self.animations.addAnimation(move_and_merge)

        self.tile_to_delete.append(moving_tile)
        pass

    def animate_random(self, pos, value):
        empty_tile = self.gui_matrix[pos[0]][pos[1]]
        tile_to_animate = gui.Tile(parent=self.grid, pos=empty_tile._pos, value=value)
        tile_to_animate.setMinimumHeight(0)
        tile_to_animate.setMinimumWidth(0)
        tile_to_animate.length = self.tile_length
        tile_to_animate.raise_()
        pop_in = QtCore.QPropertyAnimation(tile_to_animate, b"geometry")
        init_size = tile_to_animate.geometry()
        final_size = tile_to_animate.geometry()

        init_size.moveTo((2 * final_size.x() + final_size.width()) / 2,
                         (2 * final_size.y() + final_size.height()) / 2)

        init_size.setWidth(int(1))
        init_size.setHeight(int(1))

        pop_in.setStartValue(init_size)
        pop_in.setEndValue(final_size)
        pop_in.setDuration(self.animation_duration)

        self.animations.addAnimation(pop_in)
        self.tile_to_delete.append(tile_to_animate)

    def animate_tile_wobble(self, tile):
        tile_to_animate = gui.Tile(parent=self.grid, pos=tile._pos, value=tile.value)
        tile_to_animate.length = self.tile_length
        tile_to_animate.raise_()

        size_increase = QtCore.QPropertyAnimation(tile_to_animate, b"geometry")
        size_decrease = QtCore.QPropertyAnimation(tile_to_animate, b"geometry")
        init_size = tile_to_animate.geometry()
        increased_size = tile_to_animate.geometry()
        increased_size.setWidth(init_size.width() + 10)
        increased_size.setHeight(init_size.height() + 10)

        size_increase.setStartValue(init_size)
        size_increase.setEndValue(increased_size)
        size_increase.setDuration(self.animation_duration / 2)

        size_decrease.setStartValue(increased_size)
        size_decrease.setEndValue(init_size)
        size_decrease.setDuration(self.animation_duration / 2)

        wobble_animation = QtCore.QSequentialAnimationGroup()
        wobble_animation.addAnimation(size_increase)
        wobble_animation.addAnimation(size_decrease)
        self.tile_to_delete.append(tile_to_animate)
        return wobble_animation

    def clean_up(self):
        for tile in self.tile_to_delete:
            try:
                tile.deleteLater()
                tile = None
            except:
                continue

    def resizeEvent(self, QResizeEvent):
        self.tile_length = self.width() / self.grid_size + 5
        for row in self.gui_matrix:
            for tile in row:
                tile.length = self.tile_length
        self.setMinimumHeight(self.width())
        self.setMaximumHeight(self.width())


class GameGridUI(object):
    def setupUi(self, GameGrid):
        GameGrid.setObjectName("GameGrid")
        GameGrid.resize(729, 710)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(GameGrid.sizePolicy().hasHeightForWidth())
        GameGrid.setSizePolicy(sizePolicy)
        self.gridLayout = QtWidgets.QGridLayout(GameGrid)
        self.gridLayout.setObjectName("gridLayout_2")
        self.grid_frame = QtWidgets.QFrame(GameGrid)
        font = QtGui.QFont()
        font.setStyleStrategy(QtGui.QFont.PreferAntialias)
        self.grid_frame.setFont(font)
        self.grid_frame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.grid_frame.setFrameShadow(QtWidgets.QFrame.Plain)
        self.grid_frame.setObjectName("grid_frame")
        self.gridLayout.addWidget(self.grid_frame, 0, 0, 1, 1)
