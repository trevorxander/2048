from game2048 import gui
from PyQt5 import QtCore, QtWidgets, QtGui


class PlayScreen(QtWidgets.QMainWindow):
    _BACKGROUND_COLOR = QtGui.QColor.fromRgb(250, 248, 240)
    _KEY_PRESSED_SIGNAL = QtCore.pyqtSignal(QtCore.QEvent)
    _BUTTON_COLOR = 'rgb(140,123,104)'
    _BUTTON_FONT_COLOR = 'rgb(255,255,255)'
    _BUTTON_FONT_SIZE = 18
    _BUTTON_STYLE = 'QPushButton {{ background-color: {color};' \
                    'color: {font_color};' \
                    'font-size: {font_size}px;' \
                    'border: 1px solid {color};' \
                    'border-radius: 10px;}}'

    def __init__(self, parent=None, prev_screen=None, player_list=None, game_size=4, comp_difficulty=None):
        QtWidgets.QMainWindow.__init__(self)
        self._prev_screen = prev_screen
        pallete = QtGui.QPalette()
        pallete.setColor(QtGui.QPalette.Background, self._BACKGROUND_COLOR)
        self.setAutoFillBackground(True)
        self.setPalette(pallete)

        self._is_two_player = True
        if player_list is None:
            player_list = ['2048']
            self._is_two_player = False


        game_layout = QtWidgets.QHBoxLayout()
        self._running_games = []

        game = gui.GameArea(parent = self, label=player_list[0], game_size=game_size)
        self._running_games.append(game)
        game_layout.addWidget(game)


        if self._is_two_player:
            self.competition_area = gui.CompetitionArea(parent=self,
                                                        left_label=player_list[0],
                                                        right_label=player_list[1])
            game_layout.addWidget(self.competition_area)
            self.competition_area.timer_end.connect(self.end_game)

            game = gui.GameArea(parent = self,label=player_list[1], game_size=game_size)
            self._running_games.append(game)
            game_layout.addWidget(game)

        game_screen = QtWidgets.QWidget()
        game_screen.setLayout(game_layout)

        self.setCentralWidget(game_screen)


        self._player_one_keys = {QtCore.Qt.Key_Left,
                                 QtCore.Qt.Key_Right,
                                 QtCore.Qt.Key_Down,
                                 QtCore.Qt.Key_Up}

        self._player_two_keys = {QtCore.Qt.Key_A: QtCore.Qt.Key_Left ,
                                 QtCore.Qt.Key_D: QtCore.Qt.Key_Right,
                                 QtCore.Qt.Key_W: QtCore.Qt.Key_Down ,
                                 QtCore.Qt.Key_S: QtCore.Qt.Key_Up}

        self._KEY_PRESSED_SIGNAL.connect(self._running_games[0].keyPressEvent)
        self._block_input = False

        self.setStyleSheet(self._BUTTON_STYLE.format(color=self._BUTTON_COLOR,
                                                     font_color=self._BUTTON_FONT_COLOR,
                                                     font_size=self._BUTTON_FONT_SIZE))


    def _update_score(self, score_changed: tuple):
        if self._is_two_player:
            game = score_changed[0]
            new_score = score_changed[1]
            if game == self._running_games[0]:
                self.competition_area.update_left_score(new_score)
            elif game == self._running_games[1]:
                self.competition_area.update_right_score(new_score)

    def keyPressEvent(self, QKeyEvent):
        if not self._block_input:
            if QKeyEvent.key() in self._player_one_keys:
                if self._is_two_player:
                    QtCore.QCoreApplication.sendEvent(self._running_games[1], QKeyEvent)
                else:
                    QtCore.QCoreApplication.sendEvent(self._running_games[0], QKeyEvent)
            elif QKeyEvent.key() in self._player_two_keys:
                QtCore.QCoreApplication.sendEvent(self._running_games[0], QKeyEvent)

        all_game_over = True
        for games in self._running_games:
            if not games.game_model.is_game_over():
                all_game_over = False

        if all_game_over:
            self._block_input = True
            self.end_game()
        else:
            self._block_input = False


    def end_game(self):
        print('GameOver')


    def closeEvent(self, QCloseEvent):
        self._prev_screen._show_title_screen()


