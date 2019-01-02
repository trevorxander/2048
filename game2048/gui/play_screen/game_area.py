from PyQt5 import QtCore, QtGui, QtWidgets, uic
import game2048
from game2048 import gui
import time
from threading import Lock
from threading import Thread

class GameArea (QtWidgets.QWidget):

    def __init__(self, parent = None, label='2048', game_size=4, has_undo = True):
        QtWidgets.QWidget.__init__(self, parent = parent)
        self.ui = uic.loadUi('../game2048/gui/play_screen/game_area.ui', self)
        self._style = '<html><head/><body><p align="center"><span style=" font-size:{font}pt;">{value}</span></p></body></html>'
        self.ui.label.setText(self._style.format(font=50, value=label))

        self.score_label = self.ui.score
        self.score_label.set_label(self._style.format(font=15, value='Score'))
        self.set_score(self.score_label, 0)

        self.best_score_label = self.ui.best_score
        self.best_score_label.set_label( self._style.format(font=15, value='Best'))
        self.set_score(self.best_score_label,0)
        self.best_score = 0

        self.game_model = game2048.Model2048 (matrix_size=game_size)
        game_box = self.ui.game_grid_box

        self.game_grid = gui.GameGrid(matrix=self.game_model.get_matrix())
        game_box.addWidget(self.game_grid)


        self.animation_wait = Lock()
        self.resize(542,725)
        self.show()


    def set_score(self, label, score):
        label.set_value(self._style.format(font=20, value=score))


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

        def animation_complete():
            self.game_grid.clean_up()
            self.game_grid.update_grid(self.game_model.get_matrix())
            self.score = self.game_model.score
            self.set_score(self.score_label, self.score)
            if self.best_score < self.score:
                self.set_score(self.best_score_label,self.score)

        # self.game_grid.animations.clear()
        # moved_tiles = self.game_model.get_moved_tiles()
        # for movement in moved_tiles:
        #     old_loc = movement[0]
        #     new_loc = movement[1]
        #     value = movement[2]
        #     self.game_grid.animate_tile(old_loc, new_loc, value)
        # random_inserts = self.game_model.get_pop_ins()
        # for randoms in random_inserts:
        #     self.game_grid.animate_random(randoms[0],randoms[1])
        #
        # self.game_grid.animations.start()
        # self.game_grid.animations.finished.connect(animation_complete)
        animation_complete()


