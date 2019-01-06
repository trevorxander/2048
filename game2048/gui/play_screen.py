from game2048 import gui
from PyQt5 import QtCore, QtWidgets, QtGui
import queue


class PlayScreen(QtWidgets.QMainWindow):
    BACKGROUND_COLOR = QtGui.QColor.fromRgb(250, 248, 240)

    keyboard_buffer = []
    key_pressed = QtCore.pyqtSignal(QtCore.QEvent)

    def __init__(self, parent=None, prev_screen=None, player_list=None, game_size=4, comp_difficulty=None):
        QtWidgets.QMainWindow.__init__(self)

        pallete = QtGui.QPalette()
        pallete.setColor(QtGui.QPalette.Background, self.BACKGROUND_COLOR)
        self.setAutoFillBackground(True)
        self.setPalette(pallete)

        self.is_two_player = True
        if player_list is None:
            player_list = ['2048']
            self.is_two_player = False


        game_layout = QtWidgets.QHBoxLayout()
        self.running_games = []

        game = gui.GameArea(parent = self, label=player_list[0], game_size=game_size)
        self.running_games.append(game)
        game_layout.addWidget(game)


        if self.is_two_player:
            self.competition_area = gui.CompetitionArea(parent=self,
                                                        left_label=player_list[0],
                                                        right_label=player_list[1])
            game_layout.addWidget(self.competition_area)

            game = gui.GameArea(parent = self,label=player_list[1], game_size=game_size)
            self.running_games.append(game)
            game_layout.addWidget(game)

        game_screen = QtWidgets.QWidget()
        game_screen.setLayout(game_layout)

        self.setCentralWidget(game_screen)
        self.event_queue = queue.Queue(maxsize=0)

        self.player_one_keys = {QtCore.Qt.Key_Left,
                                QtCore.Qt.Key_Right,
                                QtCore.Qt.Key_Down,
                                QtCore.Qt.Key_Up}

        self.player_two_keys = {QtCore.Qt.Key_A: QtCore.Qt.Key_Left ,
                                QtCore.Qt.Key_D: QtCore.Qt.Key_Right,
                                QtCore.Qt.Key_W: QtCore.Qt.Key_Down ,
                                QtCore.Qt.Key_S: QtCore.Qt.Key_Up}

        self.key_pressed.connect(self.running_games[0].keyPressEvent)


    def update_score(self, score_changed: tuple):
        if self.is_two_player:
            game = score_changed[0]
            new_score = score_changed[1]
            if game == self.running_games[0]:
                self.competition_area.update_left_score(new_score)
            elif game == self.running_games[1]:
                self.competition_area.update_right_score(new_score)

    def keyPressEvent(self, QKeyEvent):
        if QKeyEvent.key() in self.player_one_keys:
            if self.is_two_player:
                QtCore.QCoreApplication.sendEvent(self.running_games[1], QKeyEvent)
            else:
                QtCore.QCoreApplication.sendEvent(self.running_games[0], QKeyEvent)
        elif QKeyEvent.key() in self.player_two_keys:
            QtCore.QCoreApplication.sendEvent(self.running_games[0], QKeyEvent)

    def timer_end(self):
        pass

