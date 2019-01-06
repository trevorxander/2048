from PyQt5 import QtCore, QtGui, QtWidgets
from game2048.gui.elements import Button, Label
import game2048

class TitleScreen(QtWidgets.QWidget):
    BACKGROUND_COLOR = QtGui.QColor.fromRgb(250, 248, 240)
    def __init__(self, parent=None,):
        QtWidgets.QWidget.__init__(self, parent=parent)

        self.ui = TitleScreenUI()
        self.ui.setupUi(self)

        pallete = QtGui.QPalette()
        pallete.setColor(QtGui.QPalette.Background, self.BACKGROUND_COLOR)
        self.setAutoFillBackground(True)
        self.setPalette(pallete)
        self.setMinimumWidth(540)
        self.setMinimumHeight(800)
        self.resize(self.minimumSize())

        self.two_player = ['Player 1',
                           'Player 2']

        self.with_computer = ['Player',
                              'AI']

        self.show_title_screen()

    def show_title_screen(self):
        self.hide_items(self.ui.computer_options)
        self.hide_items(self.ui.single_player_options)
        self.show()

    def start_game(self, player_names, game_size, difficulty = None):
        self.hide()
        self.hide_items(self.ui.computer_options)
        self.hide_items(self.ui.single_player_options)

        play_screen = game2048.gui.PlayScreen(parent=None,
                                              prev_screen = self,
                                              comp_difficulty = difficulty,
                                              player_list=player_names,
                                              game_size=game_size)
        play_screen.show()

    def single_player_pressed(self):
        self.show_items(self.ui.single_player_options)
        self.start_game(None, 4, None)

    def solo_pressed(self):
        pass


    def computer_pressed(self):
        self.show_items(self.ui.computer_options)

    def easy_pressed(self):
        pass

    def medium_pressed(self):
        pass

    def hard_pressed(self):
        pass

    def two_player_pressed(self):
        self.start_game(self.two_player, 4, None)

    def show_items (self,layout):
        self.setMinimumHeight(self.minimumHeight() + 90)
        self.resize(self.minimumSize())

        for item_count in range(layout.count()):
            item = layout.itemAt(item_count)
            item.widget().show()

    def hide_items(self,layout):
        self.setMinimumHeight(self.minimumHeight() - 90)
        self.resize(self.minimumSize())

        for item_count in range(layout.count()):
            item = layout.itemAt(item_count)
            item.widget().hide()

class TitleScreenUI(object):
    MAIN_LABEL_COLOR = 'rgb(118,110,102)'
    MAIN_LABEL_FONT_SIZE = 80
    MAIN_LABEL_STYLE = 'QLabel {{color: {color};' \
                       'font-size: {font_size}px; ' \
                       'font-weight: bold; }}'
    BUTTON_MIN_SIZE = QtCore.QSize(450,90)
    OPTION_BUTTON_MIN_SIZE = QtCore.QSize(220,80)
    DIFFICULTY_BUTTON_MIN_SIZE = QtCore.QSize(100,80)

    def setupUi(self, titlescreen):
        titlescreen.setObjectName("titlescreen")
        titlescreen.resize(430, 568)
        self.verticalLayout = QtWidgets.QVBoxLayout(titlescreen)
        self.verticalLayout.setObjectName("verticalLayout")

        self.main_label = QtWidgets.QLabel(titlescreen)
        self.main_label.setText('2048')
        self.main_label.setStyleSheet(self.MAIN_LABEL_STYLE.format(color=self.MAIN_LABEL_COLOR,
                                                                   font_size=self.MAIN_LABEL_FONT_SIZE))
        self.main_label.setAlignment(QtCore.Qt.AlignCenter)
        self.verticalLayout.addWidget(self.main_label)
        self.game_options = QtWidgets.QVBoxLayout()
        self.game_options.setSpacing(0)
        self.game_options.setObjectName("game_options")

        self.single_player = Button(titlescreen, text='Single Player')
        self.single_player.setObjectName("single_player")
        self.single_player.ui.pushButton.setMinimumSize(self.BUTTON_MIN_SIZE)
        self.game_options.addWidget(self.single_player)

        self.single_player_options = QtWidgets.QHBoxLayout()
        self.single_player_options.setObjectName("single_player_options")
        self.single_player.setMinimumWidth(500)
        self.single_player.setMinimumHeight(120)

        self.solo = Button(titlescreen)
        self.solo.setObjectName("solo")
        self.solo.set_text('Solo')
        self.solo.ui.pushButton.setMinimumSize(self.OPTION_BUTTON_MIN_SIZE)
        self.solo.setMinimumHeight(120)
        self.single_player_options.addWidget(self.solo)

        self.computer = Button(titlescreen)
        self.computer.setObjectName("computer")
        self.computer.set_text('vs. AI')
        self.computer.ui.pushButton.setMinimumSize(self.OPTION_BUTTON_MIN_SIZE)
        self.computer.setMinimumHeight(120)
        self.single_player_options.addWidget(self.computer)
        self.game_options.addLayout(self.single_player_options)

        self.computer_options = QtWidgets.QHBoxLayout()
        self.computer_options.setObjectName("computer_options")

        self.easy = Button(parent=titlescreen, text= 'Easy')
        self.easy.setObjectName("easy")
        self.easy.ui.pushButton.setMinimumSize(self.DIFFICULTY_BUTTON_MIN_SIZE)
        self.computer_options.addWidget(self.easy)

        self.medium = Button(parent=titlescreen, text= 'Medium')
        self.medium.setObjectName("medium")
        self.medium.ui.pushButton.setMinimumSize(self.DIFFICULTY_BUTTON_MIN_SIZE)
        self.computer_options.addWidget(self.medium)

        self.hard = Button(parent=titlescreen, text= 'Hard')
        self.hard.setObjectName("hard")
        self.hard.ui.pushButton.setMinimumSize(self.DIFFICULTY_BUTTON_MIN_SIZE)
        self.hard.setMinimumHeight(120)
        self.computer_options.addWidget(self.hard)

        self.game_options.addLayout(self.computer_options)
        self.two_player = Button(titlescreen, text='Two Players')
        self.two_player.setObjectName("two_player")
        self.two_player.ui.pushButton.setMinimumSize(self.BUTTON_MIN_SIZE)
        self.two_player.setMinimumWidth(500)
        self.two_player.setMinimumHeight(120)
        self.game_options.addWidget(self.two_player)

        self.verticalLayout.setStretch(0, 1)
        self.verticalLayout.setStretch(1, 1)
        self.verticalLayout.setStretch(2, 1)
        self.verticalLayout.setStretch(3, 1)

        self.game_options.setStretch(0, 1)
        self.game_options.setStretch(1, 1)
        self.game_options.setStretch(2, 1)
        self.game_options.setStretch(3, 1)
        self.verticalLayout.addLayout(self.game_options)

