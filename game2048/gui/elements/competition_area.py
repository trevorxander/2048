from PyQt5 import QtCore, QtGui, QtWidgets, uic

from game2048.gui.elements import Tile, Label

class CompetitionArea(QtWidgets.QWidget):
    WINNING_STYLE =''
    LOSING_STYLE = ''
    DEFAULT_STYLE = ''

    timer_end = QtCore.pyqtSignal()
    def __init__(self, parent=None, left_label='P1', right_label='P2'):
        QtWidgets.QWidget.__init__(self, parent=parent)
        self.ui = CompetitionAreaUI()
        self.ui.setupUi(self)

        self.timer = self.ui.timer
        self._left_score = 0
        self._right_score = 0

        self.timer = self.ui.timer
        self.left = self.ui.score_diff.left
        self.right = self.ui.score_diff.right

        self.left.set_label(left_label)
        self.right.set_label(right_label)

        self.timer_tick = QtCore.QTimer()
        self.timer_tick.setInterval(1000)

        self.timer_tick.timeout.connect(self.update_timer)

        self.start_time = 60
        self.current_time = self.start_time
        self.start_timer()
        self.show()

    def start_timer(self):
        self.timer.set_value(self.current_time)
        self.timer_tick.start()

    def update_timer(self):
        self.current_time -=1
        self.timer.set_value(self.current_time)
        if self.current_time == 0:
            self.timer_tick.stop()
            self.timer_end.emit()



    def update_left_score(self, score):
        self._left_score = score
        if self._left_score > self._right_score:
            pass

        self.left.set_value(self._left_score - self._right_score)
        self.right.set_value(self._right_score - self._left_score)

    def update_right_score(self, score):
        self._right_score = score
        self.left.set_value(self._left_score - self._right_score)
        self.right.set_value(self._right_score - self._left_score)



class CompetitionAreaUI(object):

    SCORE_LAYOUT_STYLE = '* {{ '
    def setupUi(self, competition_area):

        competition_area.setObjectName("competition_area")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(competition_area)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.verticalLayout = QtWidgets.QVBoxLayout()
        self.verticalLayout.setObjectName("verticalLayout")
        spacerItem = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout.addItem(spacerItem)
        self.timer = Label (parent=competition_area, label='Timer', val=600)
        self.timer.setObjectName("timer")
        self.timer.setMinimumWidth(100)
        self.timer.resize(200,50)
        self.verticalLayout.addWidget(self.timer)
        self.verticalLayout.setAlignment(self.timer, QtCore.Qt.AlignCenter)

        self.score_diff = ScoreTracker(parent=competition_area)
        self.verticalLayout.addWidget(self.score_diff)

        spacerItem1 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout.addItem(spacerItem1)

        self.verticalLayout_2.addLayout(self.verticalLayout)
        competition_area.setMaximumSize(QtCore.QSize(ScoreTrackerUI.SCORE_WIDTH * 2 - (ScoreTrackerUI.OVERLAP - 2), 500))


class ScoreTracker(QtWidgets.QWidget):
    def __init__(self, parent=None):
        QtWidgets.QWidget.__init__(self, parent=parent)
        self.ui = ScoreTrackerUI()
        self.ui.setupUi(self)
        self.show()
        self.left = self.ui.left
        self.right = self.ui.right

class ScoreTrackerUI(object):
    SCORE_WIDTH = 200
    OVERLAP = 30
    def setupUi(self, score_tracker):
        score_tracker.setObjectName("score_tracker")
        score_tracker.resize(self.SCORE_WIDTH * 2 - (self.OVERLAP - 2), 107)
        score_tracker.setMinimumSize(QtCore.QSize(self.SCORE_WIDTH * 2 - (self.OVERLAP - 2),100))

        self.left = Label(parent=score_tracker, label='P1')
        self.left.setGeometry(QtCore.QRect(0, 0, self.SCORE_WIDTH, 100))
        self.left.setMinimumSize(QtCore.QSize(100, 100))
        self.left.setObjectName("left")

        self.right = Label(parent=score_tracker, label='P2')
        self.right.stackUnder(self.left)
        self.right.setGeometry(QtCore.QRect(self.SCORE_WIDTH - self.OVERLAP, 0, self.SCORE_WIDTH, 100))
        self.right.setMinimumSize(QtCore.QSize(0, 100))
        self.right.setObjectName("right")

        QtCore.QMetaObject.connectSlotsByName(score_tracker)