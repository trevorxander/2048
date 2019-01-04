from PyQt5 import QtCore, QtGui, QtWidgets, uic
import game2048
from game2048 import gui
import time
import queue
class GameArea (QtWidgets.QWidget):
    MARGIN = 25
    # zero for infinite buffer size
    INPUT_BUFFER_SIZE = 5
    def __init__(self, parent = None, label='2048', game_size=8, has_undo = True):
        QtWidgets.QWidget.__init__(self, parent = parent)
        self.parent = parent

        main_label_color = 'rgb(118,110,102)'
        main_label_font_size = 50

        self.ui = uic.loadUi('game2048/gui/play_screen/game_area.ui', self)
        self.main_label = self.ui.label

        self.default_style = 'QLabel {{color: {color};' \
                             'font-size: {font_size} }}'
        self.main_label.setStyleSheet(self.default_style.format(color = main_label_color,
                                                                font_size = main_label_font_size))
        self.score_label = self.ui.score
        self.best_score_label = self.ui.best_score

        self.score_label.set_label('Score')
        self.best_score_label.set_label('Best')

        self.ui.new_game.set_text('New Game')
        self.ui.undo.set_text('Undo')
        self.ui.undo.setMaximumWidth(self.ui.undo.width())


        game_box = self.ui.game_grid_box


        self.set_score(self.score_label, 0)

        self.best_score = 0
        self.set_score(self.best_score_label, 0)

        self.game_model = game2048.Model2048 (matrix_size=game_size)


        self.game_grid = gui.GameGrid(matrix=self.game_model.get_matrix())
        self.game_grid.animations.finished.connect(self.animation_complete)

        game_box.addWidget(self.game_grid)

        pallete = QtGui.QPalette()
        pallete.setColor(QtGui.QPalette.Background ,QtGui.QColor.fromRgb(250,248,240))
        self.setAutoFillBackground(True)
        self.setPalette(pallete)

        self.resize(421 + 24, 605)

        self.event_queue = queue.Queue(maxsize=self.INPUT_BUFFER_SIZE)
        self.keyboard_to_game_event = {QtCore.Qt.Key_Left: self.game_model.left,
                                  QtCore.Qt.Key_Right: self.game_model.right,
                                  QtCore.Qt.Key_Up: self.game_model.up,
                                  QtCore.Qt.Key_Down: self.game_model.down,
                                  QtCore.Qt.Key_Space: self.game_model.undo}

        self.show()

    def set_score(self, label, score):
        label.set_value(score)

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

    def undo_last_move(self):
        self.game_model.undo()
        self.game_grid.update_grid(self.game_model.get_matrix())

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
            self.game_grid.animate_random(randoms[0],randoms[1])

        self.installEventFilter(self)
        self.game_grid.animations.start()

    def keyPressEvent(self, event):
        self.event_queue.put(self.keyboard_to_game_event[event.key()])
        self.process_queued_events()

    def eventFilter(self, QObject, QEvent):
        if (QEvent.type() == QtCore.QEvent.KeyPress):
            if(QEvent.key() in self.keyboard_to_game_event):
                if self.event_queue.full():
                    return True
                self.event_queue.put(self.keyboard_to_game_event[QEvent.key()])
            return True
        return False

    def process_queued_events(self):
        if self.event_queue.empty():
            self.removeEventFilter(self)
        else:
            self.event_queue.get()()
            self.update_game()

    def animation_complete(self):
        self.game_grid.clean_up()
        self.game_grid.update_grid(self.game_model.get_matrix())
        self.score = self.game_model.score
        self.set_score(self.score_label, self.score)
        if self.best_score < self.score:
            self.set_score(self.best_score_label, self.score)

        self.process_queued_events()





