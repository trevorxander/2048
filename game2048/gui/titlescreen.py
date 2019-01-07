from PyQt5 import QtCore, QtGui, QtWidgets
from game2048.gui.elements import Label
import game2048

class TitleScreen(QtWidgets.QWidget):
    _BACKGROUND_COLOR = QtGui.QColor.fromRgb(250, 248, 240)
    _BUTTON_COLOR = 'rgb(140,123,104)'
    _BUTTON_ACTIVE_COLOR = 'rgb(99, 87, 73)'
    _BUTTON_FONT_COLOR = 'rgb(255,255,255)'
    _BUTTON_FONT_SIZE = 18
    _BUTTON_SYLE = 'QPushButton {{ background-color: {color};' \
                    'color: {font_color};' \
                    'font-size: {font_size}px;' \
                    'border: 1px solid {color};' \
                    'border-radius: 10px;}}'


    def __init__(self, parent=None):
        QtWidgets.QWidget.__init__(self, parent=parent)

        self._ui = TitleScreenUI()
        self._ui.setupUi(self)

        pallete = QtGui.QPalette()
        pallete.setColor(QtGui.QPalette.Background, self._BACKGROUND_COLOR)
        self.setAutoFillBackground(True)
        self.setPalette(pallete)
        self.setMinimumWidth(540)
        self.setMinimumHeight(800)
        self.resize(self.minimumSize())

        self._two_player = ['Player 1',
                           'Player 2']

        self._with_computer = ['Player',
                              'AI']

        self.setStyleSheet(self._BUTTON_SYLE.format(color=self._BUTTON_COLOR,
                                                    font_color=self._BUTTON_FONT_COLOR,
                                                    font_size=self._BUTTON_FONT_SIZE))

        self._game_args = {'prev_screen': self,
                          'player_list': None,
                          'game_size': 4,
                          'comp_difficulty': None}

        self.setup_button_connection()
        self._show_title_screen()

    def setup_button_connection(self):
        self._ui.single_player.pressed.connect(self._single_player_pressed)
        self._ui.two_player.pressed.connect(self._two_player_pressed)
        self._ui.grid_options_button.pressed.connect(self._grid_options_pressed)
        self._ui.computer.pressed.connect(self._computer_pressed)
        self._ui.easy.pressed.connect(self._easy_pressed)
        self._ui.medium.pressed.connect(self._medium_pressed)
        self._ui.hard.pressed.connect(self._hard_pressed)
        self._ui.solo.pressed.connect(self._solo_pressed)
        self._ui.start_game.pressed.connect(self._start_game)
        self._ui.four.pressed.connect(self._four_pressed)
        self._ui.five.pressed.connect(self._five_pressed)
        self._ui.six.pressed.connect(self._six_pressed)

    def _show_title_screen(self):
        self._hide_items(self._ui.computer_options)
        self._hide_items(self._ui.single_player_options)
        self._hide_items(self._ui.player_name_options)
        self._hide_items(self._ui.grid_options)

        self._single_player_pressed()
        self.show()


    def _start_game(self):
        self.hide()
        self._hide_items(self._ui.computer_options)
        self._hide_items(self._ui.single_player_options)
        self._hide_items(self._ui.player_name_options)
        self._hide_items(self._ui.grid_options)


        if self._game_args['player_list'] is not None:
            if self._ui.player_one_input.text() != '':
                self._game_args['player_list'][0] =  self._ui.player_one_input.text()
            if self._ui.player_two_input.text() != '':
                self._game_args['player_list'][1] = self._ui.player_two_input.text()



        play_screen = game2048.gui.PlayScreen(**self._game_args)
        play_screen.show()

    def _actiate_button(self, button):
        button.setStyleSheet(self._BUTTON_SYLE.format(color=self._BUTTON_ACTIVE_COLOR,
                                                      font_color=self._BUTTON_FONT_COLOR,
                                                      font_size=self._BUTTON_FONT_SIZE))

    def _deactivate_button(self, button):
        button.setStyleSheet(self._BUTTON_SYLE.format(color=self._BUTTON_COLOR,
                                                      font_color=self._BUTTON_FONT_COLOR,
                                                      font_size=self._BUTTON_FONT_SIZE))


    def _single_player_pressed(self):
        self._actiate_button(self._ui.single_player)
        self._deactivate_button(self._ui.two_player)
        self._deactivate_button(self._ui.computer)
        self._show_items(self._ui.single_player_options)
        self._hide_items(self._ui.player_name_options)
        self._solo_pressed()

    def _solo_pressed(self):
        self._actiate_button(self._ui.solo)
        self._deactivate_button(self._ui.computer)
        self._hide_items(self._ui.computer_options)
        self._game_args['player_list'] = None
        self._game_args['comp_difficulty'] = None


    def _computer_pressed(self):
        self._actiate_button(self._ui.computer)
        self._deactivate_button(self._ui.solo)
        self._game_args['player_list'] = ['Player',
                                        'AI']
        self._easy_pressed()
        self._show_items(self._ui.computer_options)


    def _easy_pressed(self):
        self._actiate_button(self._ui.easy)
        self._deactivate_button(self._ui.medium)
        self._deactivate_button(self._ui.hard)
        self._game_args['comp_difficulty'] = 0

    def _medium_pressed(self):
        self._deactivate_button(self._ui.easy)
        self._actiate_button(self._ui.medium)
        self._deactivate_button(self._ui.hard)
        self._game_args['comp_difficulty'] = 1

    def _hard_pressed(self):
        self._deactivate_button(self._ui.easy)
        self._deactivate_button(self._ui.medium)
        self._actiate_button(self._ui.hard)
        self._game_args['comp_difficulty'] = 2

    def _grid_options_pressed(self):
        self._show_items(self._ui.grid_options)
        self._four_pressed()

    def _four_pressed(self):
        self._actiate_button(self._ui.four)
        self._deactivate_button(self._ui.five)
        self._deactivate_button(self._ui.six)
        self._change_grid_size(4)

    def _five_pressed(self):
        self._deactivate_button(self._ui.four)
        self._actiate_button(self._ui.five)
        self._deactivate_button(self._ui.six)
        self._change_grid_size(5)

    def _six_pressed(self):
        self._deactivate_button(self._ui.four)
        self._deactivate_button(self._ui.five)
        self._actiate_button(self._ui.six)
        self._change_grid_size(6)

    def _two_player_pressed(self):
        self._actiate_button(self._ui.two_player)
        self._deactivate_button(self._ui.single_player)
        self._hide_items(self._ui.single_player_options)
        self._hide_items(self._ui.computer_options)
        self._show_items(self._ui.player_name_options)
        self._game_args['player_list'] = ['Player 1',
                                         'Player 2']

    def _change_grid_size(self, grid_size):
        self._game_args['game_size'] = grid_size

    def _show_items (self, layout):
        self.resize(self.minimumSize())
        for item_count in range(layout.count()):
            item = layout.itemAt(item_count)
            item.widget().show()

    def _hide_items(self, layout):
        self.resize(self.minimumSize())

        for item_count in range(layout.count()):
            item = layout.itemAt(item_count)
            item.widget().hide()

class TitleScreenUI(object):
    MAIN_LABEL_COLOR = 'rgb(118,110,102)'
    MAIN_LABEL_FONT_SIZE = 80
    MAIN_LABEL_SIZE = QtCore.QSize(0,0)
    MAIN_LABEL_STYLE = 'QLabel {{color: {color};' \
                       'font-size: {font_size}px; ' \
                       'font-weight: bold; }}'
    BUTTON_MIN_SIZE = QtCore.QSize(450,80)
    OPTION_BUTTON_MIN_SIZE = QtCore.QSize(220,50)
    DIFFICULTY_BUTTON_MIN_SIZE = QtCore.QSize(100,50)

    def setupUi(self, titlescreen):
        titlescreen.setObjectName("titlescreen")
        self.main_layout = QtWidgets.QVBoxLayout(titlescreen)
        self.main_layout.setObjectName("main_layout")

        self.main_label = QtWidgets.QLabel(titlescreen)
        self.main_label.setText('2048')
        self.main_label.resize(self.MAIN_LABEL_SIZE)
        self.main_label.setStyleSheet(self.MAIN_LABEL_STYLE.format(color=self.MAIN_LABEL_COLOR,
                                                                   font_size=self.MAIN_LABEL_FONT_SIZE))
        self.main_label.setAlignment(QtCore.Qt.AlignCenter)
        self.main_layout.addWidget(self.main_label)

        self.game_options = QtWidgets.QVBoxLayout()
        self.game_options.setSpacing(-1)
        self.game_options.setObjectName("game_options")

        self.single_player = QtWidgets.QPushButton(titlescreen)
        self.single_player.setText('Single Player')
        self.single_player.setObjectName("single_player")
        self.single_player.setMinimumSize(self.BUTTON_MIN_SIZE)
        self.game_options.addWidget(self.single_player)

        self.single_player_options = QtWidgets.QHBoxLayout()
        self.single_player_options.setObjectName("single_player_options")


        self.solo = QtWidgets.QPushButton(titlescreen)
        self.solo.setObjectName("solo")
        self.solo.setText('Solo')
        self.solo.setMinimumSize(self.OPTION_BUTTON_MIN_SIZE)
        self.single_player_options.addWidget(self.solo)

        self.computer = QtWidgets.QPushButton(titlescreen)
        self.computer.setObjectName("computer")
        self.computer.setText('vs. AI')
        self.computer.setMinimumSize(self.OPTION_BUTTON_MIN_SIZE)
        self.single_player_options.addWidget(self.computer)
        self.game_options.addLayout(self.single_player_options)

        self.computer_options = QtWidgets.QHBoxLayout()
        self.computer_options.setObjectName("computer_options")

        self.easy = QtWidgets.QPushButton(titlescreen)
        self.easy.setText('Easy')
        self.easy.setObjectName("easy")
        self.easy.setMinimumSize(self.DIFFICULTY_BUTTON_MIN_SIZE)
        self.computer_options.addWidget(self.easy)

        self.medium = QtWidgets.QPushButton(titlescreen)
        self.medium.setText('Medium')
        self.medium.setObjectName("medium")
        self.medium.setMinimumSize(self.DIFFICULTY_BUTTON_MIN_SIZE)
        self.computer_options.addWidget(self.medium)

        self.hard = QtWidgets.QPushButton(titlescreen)
        self.hard.setText('Hard')
        self.hard.setObjectName("hard")
        self.hard.setMinimumSize(self.DIFFICULTY_BUTTON_MIN_SIZE)
        self.computer_options.addWidget(self.hard)

        self.game_options.addLayout(self.computer_options)

        self.game_options.addSpacing(20)

        self.two_player = QtWidgets.QPushButton()
        self.two_player.setText('Two Players')

        self.two_player.setObjectName("two_player")
        self.two_player.setMinimumSize(self.BUTTON_MIN_SIZE)
        self.game_options.addWidget(self.two_player)

        self.player_name_options = QtWidgets.QFormLayout()
        self.player_name_options.setObjectName("player_name_options")

        self.player_one_label = QtWidgets.QLabel()
        self.player_one_label.setText('Player 1')
        self.player_one_label.setStyleSheet(self.MAIN_LABEL_STYLE.format(color=self.MAIN_LABEL_COLOR,
                                                                         font_size=30))

        self.player_one_input = QtWidgets.QLineEdit()
        self.player_one_input.setMinimumSize(200, 35)
        self.player_one_input.setStyleSheet('* {{ background-color: {color};' \
                                             'border: 1px solid {color};' \
                                             'font-size: {font}px;' \
                                             'border-radius: 10px;}}'
                                            .format(color='rgb(185,173,162)',
                                                    font= 20))
        self.player_one_input.setPlaceholderText('Player 1')
        self.player_name_options.addRow(self.player_one_label, self.player_one_input)

        self.player_two_label = QtWidgets.QLabel()
        self.player_two_label.setText('Player 2')
        self.player_two_label.setStyleSheet(self.player_one_label.styleSheet())
        self.player_two_input = QtWidgets.QLineEdit()
        self.player_two_input.setMinimumSize(200,35)
        self.player_two_input.setStyleSheet(self.player_one_input.styleSheet())
        self.player_two_input.setPlaceholderText('Player 2')

        self.player_name_options.addRow(self.player_two_label, self.player_two_input)

        self.player_name_options.setHorizontalSpacing(20)
        self.player_name_options.setLabelAlignment(QtCore.Qt.AlignLeft)

        self.game_options.addLayout(self.player_name_options)

        self.game_options.addSpacing(10)


        self.grid_options_button = QtWidgets.QPushButton(titlescreen)
        self.grid_options_button.setText('Grid Options')
        self.grid_options_button.setObjectName("Grid Options Button")
        self.grid_options_button.setMinimumSize(self.BUTTON_MIN_SIZE)
        self.game_options.addWidget(self.grid_options_button)

        self.grid_options = QtWidgets.QHBoxLayout()
        self.grid_options.setObjectName("grid_options")

        self.four = QtWidgets.QPushButton()
        self.four.setText('4X4')
        self.four.setObjectName("four")
        self.four.setMinimumSize(self.DIFFICULTY_BUTTON_MIN_SIZE)
        self.grid_options.addWidget(self.four)

        self.five = QtWidgets.QPushButton()
        self.five.setText('5X5')
        self.five.setObjectName("five")
        self.five.setMinimumSize(self.DIFFICULTY_BUTTON_MIN_SIZE)
        self.grid_options.addWidget(self.five)

        self.six = QtWidgets.QPushButton()
        self.six.setText('6X6')
        self.six.setObjectName("six")
        self.six.setMinimumSize(self.DIFFICULTY_BUTTON_MIN_SIZE)
        self.grid_options.addWidget(self.six)

        self.game_options.addLayout(self.grid_options)

        self.start_game = QtWidgets.QPushButton(titlescreen)
        self.start_game.setText('Start Game')
        self.start_game.setObjectName("Start Game")
        self.start_game.setMinimumSize(self.BUTTON_MIN_SIZE)

        self.game_options.addSpacing(70)

        self.game_options.addWidget(self.start_game)


        self.main_layout.addLayout(self.game_options)



