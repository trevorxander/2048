from game2048.ai.ai import AI
from game2048.gui.game.game_area import GameArea
from PyQt5 import QtCore, QtWidgets, QtGui
from threading import Thread
import time


class Interface(QtCore.QObject):
    movement_signal = QtCore.pyqtSignal(QtGui.QKeyEvent)
    def __init__(self, play_screen, difficulty):
        QtCore.QObject.__init__(self)

        self._ai_delay = (1.001 - (difficulty / 3 )) * 1000
        self.play_screen = play_screen
        self.movement_signal.connect(self.play_screen.process_ai_movement)
        self.direction_event_map =  {'left': QtCore.Qt.Key_Left,
                                    'right': QtCore.Qt.Key_Right,
                                    'up': QtCore.Qt.Key_Up,
                                    'down': QtCore.Qt.Key_Down}

        self.wait = QtCore.QEventLoop()
        self.event_processing = False
        self.play_screen.get_ai_game().movement_complete.connect(self.movement_processed)
        self.ai = AI(self)

    def send_event(self, direction):
        self.event = QtGui.QKeyEvent(QtCore.QEvent.KeyPress,
                                self.direction_event_map[direction],
                                QtCore.Qt.NoModifier)
        self.movement_signal.emit(self.event)
        self.event_processing = True


    def get_result(self):
        if self.event_processing:
            self.wait_for_movement()
        self.event_processing = False
        return self.play_screen.get_ai_game().game_model

    def wait_for_movement(self):
        self.wait = QtCore.QEventLoop()
        self.wait.exec()

    @QtCore.pyqtSlot()
    def start_movements(self):
        self.timer_tick = QtCore.QTimer()
        self.timer_tick.setInterval(self._ai_delay)
        self.timer_tick.timeout.connect(self.request_move)
        self.timer_tick.start()

    def stop_movements(self):
        pass

    def request_move(self):
        self.ai.make_move()

    @QtCore.pyqtSlot()
    def movement_processed(self):
        self.event_processing = False
        if self.wait.isRunning():
            self.wait.quit()





