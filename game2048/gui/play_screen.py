from game2048.ai.interface import InterfaceGUI
from game2048.gui.board import GameArea, CompetitionArea

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

    start_ai_signal = QtCore.pyqtSignal()
    def __init__(self, parent=None, prev_screen=None, player_list=None, game_size=4, comp_difficulty=None):
        QtWidgets.QMainWindow.__init__(self)
        self._prev_screen = prev_screen
        pallete = QtGui.QPalette()
        pallete.setColor(QtGui.QPalette.Background, self._BACKGROUND_COLOR)
        self.setAutoFillBackground(True)
        self.setPalette(pallete)

        self.setStyleSheet(self._BUTTON_STYLE.format(color=self._BUTTON_COLOR,
                                                     font_color=self._BUTTON_FONT_COLOR,
                                                     font_size=self._BUTTON_FONT_SIZE))

        self.wait = QtCore.QEventLoop()
        self._is_two_player = True
        if player_list is None:
            player_list = ['2048']
            self._is_two_player = False

        self.vs_computer = False
        if self._is_two_player and player_list[1] == 'AI':
            self.vs_computer=True


        game_layout = QtWidgets.QHBoxLayout()
        self._running_games = []

        game = GameArea(parent = self, label=player_list[0], game_size=game_size)
        self._running_games.append(game)
        game_layout.addWidget(game)


        if self._is_two_player:
            self.competition_area = CompetitionArea(parent=self,
                                                        left_label=player_list[0],
                                                        right_label=player_list[1])
            game_layout.addWidget(self.competition_area)
            self.competition_area.timer_end.connect(self._game_over)
            game = GameArea(parent = self,
                                label=player_list[1],
                                game_size=game_size,
                                has_new_game=False)

            self._running_games.append(game)
            game_layout.addWidget(game)

        if self.vs_computer:
            self.vs_computer = True
            self.installEventFilter(self)
            self.ai_interface = InterfaceGUI(self, comp_difficulty)
            self.ai_thread = QtCore.QThread()
            self.ai_interface.moveToThread(self.ai_thread)
            self.ai_thread.finished.connect(self.ai_interface.deleteLater)
            self.start_ai_signal.connect(self.ai_interface.start_movements)

        game_screen = QtWidgets.QWidget()
        game_screen.setLayout(game_layout)

        self.setCentralWidget(game_screen)




        self._player_two_keys = {QtCore.Qt.Key_Left,
                                 QtCore.Qt.Key_Right,
                                 QtCore.Qt.Key_Down,
                                 QtCore.Qt.Key_Up}

        self._player_one_keys = {QtCore.Qt.Key_A: QtCore.Qt.Key_Left ,
                                 QtCore.Qt.Key_D: QtCore.Qt.Key_Right,
                                 QtCore.Qt.Key_W: QtCore.Qt.Key_Down ,
                                 QtCore.Qt.Key_S: QtCore.Qt.Key_Up}

        self._KEY_PRESSED_SIGNAL.connect(self._running_games[0].keyPressEvent)
        self._block_input = False


    def _new_game_event(self):
        self._block_input = False
        if self._is_two_player:
            self.competition_area.start_timer()
            self._running_games[1]._start_game()

    def _update_score(self, score_changed: tuple):
        if self._is_two_player:
            game = score_changed[0]
            new_score = score_changed[1]
            if game == self._running_games[0]:
                self.competition_area.update_left_score(new_score)
            elif game == self._running_games[1]:
                self.competition_area.update_right_score(new_score)

    @QtCore.pyqtSlot (QtGui.QKeyEvent)
    def process_ai_movement(self, movement_event):
        if not self._block_input:
            self.event = movement_event
            QtCore.QCoreApplication.sendEvent(self._running_games[1], self.event)

    def get_ai_game(self):
        return self._running_games[1]

    def keyPressEvent(self, QKeyEvent):
        if not self._block_input:
            if self._is_two_player:
                if QKeyEvent.key() in self._player_one_keys:
                    QtCore.QCoreApplication.sendEvent(self._running_games[0], QKeyEvent)
                elif QKeyEvent.key() in self._player_two_keys:
                    QtCore.QCoreApplication.sendEvent(self._running_games[1], QKeyEvent)
            else:
                for games in self._running_games:
                    QtCore.QCoreApplication.sendEvent(games, QKeyEvent)

            self._check_game_over()

    def eventFilter(self, QObject, QEvent):
        if QEvent.type() == QtCore.QEvent.KeyPress:
            if QEvent.key() in self._player_two_keys:
                if not self._block_input:
                    QtCore.QCoreApplication.sendEvent(self._running_games[0], QEvent)
                return True
        return False

    def _check_game_over(self):
        all_game_over = True
        for games in self._running_games:
            if not games._game_model.is_game_over():
                all_game_over = False

        if all_game_over:
            self._game_over()
        else:
            if not self._is_two_player:
                self._block_input = False


    def _game_over(self):
        self._block_input = True

    def showEvent(self, QShowEvent):
        QtWidgets.QMainWindow.show(self)
        if self._is_two_player:
            self.competition_area.start_timer()
            if self.vs_computer:
                self.ai_thread.start()
                self.start_ai_signal.emit()


    def closeEvent(self, QCloseEvent):
        self._prev_screen._show_title_screen()


