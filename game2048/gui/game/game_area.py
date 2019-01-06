from PyQt5 import QtCore, QtGui, QtWidgets
from game2048.gui.elements import Button, Label
from game2048 import gui
import game2048
import queue


class GameArea(QtWidgets.QWidget):
    MARGIN = 25
    BACKGROUND_COLOR = QtGui.QColor.fromRgb(250, 248, 240)
    MAIN_LABEL_COLOR = 'rgb(118,110,102)'
    MAIN_LABEL_FONT_SIZE = 55
    MAIN_LABEL_STYLE = 'QLabel {{color: {color};' \
                       'font-size: {font_size}px; ' \
                       'font-weight: bold; }}'
    DEFAULT_STYLE = 'game_area {{ background-color: {color};' \
                    'border: 1px solid {color};' \
                    'border-radius: 10px;}}'

    # zero for infinite buffer size
    INPUT_BUFFER_SIZE = 0

    score_changed_signal = QtCore.pyqtSignal(tuple)

    def __init__(self, parent=None, label='2048', game_size=4, has_undo=True):
        QtWidgets.QWidget.__init__(self, parent=parent)

        self.parent = parent
        main_label_font_size = self.MAIN_LABEL_FONT_SIZE - len(label) * 2

        pallete = QtGui.QPalette()
        pallete.setColor(QtGui.QPalette.Background, self.BACKGROUND_COLOR)
        self.setAutoFillBackground(True)
        self.setPalette(pallete)

        self.ui = GameAreaUI()
        self.ui.setupUi(self)

        self.main_label = self.ui.label
        self.main_label.setStyleSheet(self.MAIN_LABEL_STYLE.format(color=self.MAIN_LABEL_COLOR,
                                                                   font_size=main_label_font_size))
        self.main_label.setText(label)

        self.score_label = self.ui.score
        self.best_score_label = self.ui.best_score
        self.score_label.set_label('Score')
        self.best_score_label.set_label('Best')
        self._score = 0
        self.best_score = 0
        self.set_score(0)
        self.set_score(0)

        self.ui.new_game.set_text('New Game')
        self.ui.undo.set_text('Undo')

        if not has_undo:
            self.ui.undo.hide()

        self.ui.undo.setMaximumWidth(self.ui.undo.width())

        self.game_model = game2048.Model2048(matrix_size=game_size)
        self.game_grid = gui.GameGrid(matrix=self.game_model.get_matrix())
        self.game_grid.animations.finished.connect(self.update_screen)
        game_box = self.ui.game_grid_box
        game_box.addWidget(self.game_grid)

        self.event_queue = queue.Queue(maxsize=self.INPUT_BUFFER_SIZE)
        self.keyboard_to_game_event = {QtCore.Qt.Key_Left: self.game_model.left,
                                       QtCore.Qt.Key_Right: self.game_model.right,
                                       QtCore.Qt.Key_Up: self.game_model.up,
                                       QtCore.Qt.Key_Down: self.game_model.down,
                                       QtCore.Qt.Key_A: self.game_model.left,
                                       QtCore.Qt.Key_D: self.game_model.right,
                                       QtCore.Qt.Key_W: self.game_model.up,
                                       QtCore.Qt.Key_S: self.game_model.down}

        self.setMaximumWidth(self.game_grid.maximumWidth())

        self.score_changed_signal.connect(parent.update_score)

        self.show()

    def set_score(self, score):
        if score == self._score:
            return
        self._score = score
        self.score_label.set_value(score)
        if score > self.best_score:
            self.best_score = score
            self.best_score_label.set_value(score)
        self.score_changed_signal.emit((self,score))


    def new_game(self):
        self.game_model.restart_game()
        self.update_screen()

    def undo(self):
        self.game_model.undo()
        self.update_screen()

    def update_game(self):
        self.game_grid.animations.clear()
        moved_tiles = self.game_model.get_moved_tiles()
        for movement in moved_tiles:
            old_loc = movement[0]
            new_loc = movement[1]
            value = movement[2]
            self.game_grid.animate_tile(old_loc, new_loc, value)
        random_inserts = self.game_model.get_pop_ins()
        for randoms in random_inserts:
            self.game_grid.animate_random(randoms[0], randoms[1])

        self.installEventFilter(self)
        self.game_grid.animations.start()

    def keyPressEvent(self, event):
        self.event_queue.put(self.keyboard_to_game_event[event.key()])
        self.process_queued_events()

    def eventFilter(self, QObject, QEvent):
        if (QEvent.type() == QtCore.QEvent.KeyPress):
            if (QEvent.key() in self.keyboard_to_game_event):
                if self.event_queue.full():
                    return True
                self.game_grid.animation_duration = 50
                self.event_queue.put(self.keyboard_to_game_event[QEvent.key()])
            return True
        return False

    def process_queued_events(self):
        if self.event_queue.empty():
            self.removeEventFilter(self)
            self.game_grid.animation_duration = self.game_grid.DEFAULT_ANIMATION_DURATION
        else:
            self.event_queue.get()()
            self.update_game()

    def update_screen(self):
        self.game_grid.clean_up()
        self.game_grid.update_grid(self.game_model.get_matrix())
        self.set_score(self.game_model.score)

        self.process_queued_events()

class GameAreaUI(object):
    def setupUi(self, game_area):
        game_area.setObjectName("game_area")
        game_area.resize(862, 678)
        game_area.setMinimumSize(QtCore.QSize(0, 0))
        game_area.setSizeIncrement(QtCore.QSize(0, 0))
        game_area.setBaseSize(QtCore.QSize(0, 0))
        game_area.setStyleSheet("gamewindow{ background: rgb(250, 248, 240)}")
        self.gridLayout = QtWidgets.QGridLayout(game_area)
        self.gridLayout.setObjectName("gridLayout")
        self.game_board = QtWidgets.QVBoxLayout()
        self.game_board.setSpacing(0)
        self.game_board.setObjectName("game_board")
        self.game_header = QtWidgets.QHBoxLayout()
        self.game_header.setSpacing(0)
        self.game_header.setObjectName("game_header")
        self.label = QtWidgets.QLabel(game_area)
        self.label.setObjectName("label")
        self.label.setAlignment(QtCore.Qt.AlignCenter)
        self.game_header.addWidget(self.label)
        self.verticalLayout = QtWidgets.QVBoxLayout()
        self.verticalLayout.setSpacing(0)
        self.verticalLayout.setObjectName("verticalLayout")
        self.score_layout = QtWidgets.QHBoxLayout()
        self.score_layout.setSpacing(0)
        self.score_layout.setObjectName("score_layout")
        self.score = Label(game_area)
        self.score.setObjectName("score")
        self.score_layout.addWidget(self.score)
        self.best_score = Label(game_area)
        self.best_score.setObjectName("best_score")
        self.score_layout.addWidget(self.best_score)
        self.score_layout.setStretch(0, 1)
        self.score_layout.setStretch(1, 1)
        self.verticalLayout.addLayout(self.score_layout)
        self.button_layout = QtWidgets.QHBoxLayout()
        self.button_layout.setSpacing(10)
        self.button_layout.setObjectName("button_layout")
        self.new_game = Button(game_area)
        self.new_game.setObjectName("new_game")
        self.button_layout.addWidget(self.new_game)
        self.undo = Button(game_area)
        self.undo.setObjectName("undo")
        self.button_layout.addWidget(self.undo)
        self.button_layout.setStretch(0, 2)
        self.button_layout.setStretch(1, 1)
        self.verticalLayout.addLayout(self.button_layout)
        self.verticalLayout.setStretch(0, 1)
        self.verticalLayout.setStretch(1, 1)
        self.game_header.addLayout(self.verticalLayout)
        self.game_header.setStretch(0, 1)
        self.game_header.setStretch(1, 2)
        self.game_board.addLayout(self.game_header)
        self.game_grid_box = QtWidgets.QHBoxLayout()
        self.game_grid_box.setObjectName("game_grid_box")
        self.game_board.addLayout(self.game_grid_box)
        self.game_board.setStretch(0, 1)
        self.game_board.setStretch(1, 4)
        self.gridLayout.addLayout(self.game_board, 0, 0, 1, 1)