from PyQt5 import QtCore, QtGui, QtWidgets, uic

class Label (QtWidgets.QWidget):

    def __init__(self, parent = None, Label='test', val = 0):
        QtWidgets.QWidget.__init__(self, parent = parent)

        self.ui = uic.loadUi('game2048/gui/elements/label.ui', self)
        self._label = self.ui.label
        self._value = self.ui.value
        label_color = 'rgb(185,173,162)'
        label_font_color = 'rgb(255,255,255)'
        value_font_size = 30
        label_font_size = 15

        self.default_style = '* {{ background-color: {color};' \
                                 'border: 1px solid {color};' \
                                 'border-radius: 10px;}}'
        self.setStyleSheet(self.default_style.format(color=label_color))

        self._label_style = '* {{ color: {color};' \
                                'font-size: {font_size}px  }}'

        self.label.setStyleSheet(self._label_style.format(color=label_font_color,
                                                          font_size=label_font_size))
        self._value.setStyleSheet(self._label_style.format(color=label_font_color,
                                                           font_size=value_font_size))


        self.show()

    def set_label(self, label):
        self._label.setText(str(label))
        pass


    def set_value(self, value):
        self._value.setText(str(value))
        pass


class Button (QtWidgets.QWidget):
    def __init__(self, parent = None, text=''):
        QtWidgets.QWidget.__init__(self, parent = parent)
        self.ui = uic.loadUi('game2048/gui/elements/button.ui', self)

        color = 'rgb(140,123,104)'
        font_color = 'rgb(255,255,255)'
        font_size = 18
        self.default_style = '* {{ background-color: {color};' \
                             'color: {font_color};' \
                             'font-size: {font_size}px;' \
                             'border: 1px solid {color};' \
                             'border-radius: 10px;}}'
        self.setStyleSheet(self.default_style.format(color=color,
                                                     font_color=font_color,
                                                     font_size=font_size))

        self.show()

    def set_text(self, button_text):
        self.ui.pushButton.setText(button_text)


class Tile (QtWidgets.QWidget):
    GRID_SPACING = 16
    def __init__(self, parent = None, value=0, pos = (0,0)):
        self.parent = parent
        self._game_size = parent.parent().grid_size

        self._pos = pos
        self._value = value
        QtWidgets.QWidget.__init__(self, parent = parent)
        ui = uic.loadUi('game2048/gui/elements/tile.ui', self)
        self._value_label = ui.value_label


        self._all_styles = {}
        self.default_style = 'QLabel {{background-color: {color};' \
                                    'color: {font_color};' \
                                    'font-size: {font_size}px;' \
                                    'border: 1px solid {color};' \
                                    'font-weight: bold;' \
                                    'border-radius: 10px;}}'
        base = 2
        for exp in range(1,12):
            tile_value = base ** exp
            self._all_styles[tile_value] = 'Style {0}'.format(tile_value)

        self._value_label.setAlignment(QtCore.Qt.AlignCenter)
        self._all_styles[0] = {'color':'rgb(200,193,181)',
                               'font_color':'rgb(0,0,0)',
                               'font_size':48}
        self._all_styles[2] = {'color':'rgb(236,228,219)',
                               'font_color':'rgb(115,107,100)',
                               'font_size':48}
        self._all_styles[4] = {'color': 'rgb(234,224,202)',
                               'font_color': 'rgb(115,107,100)',
                               'font_size': 48}
        self._all_styles[8] = {'color': 'rgb(232,179,129)',
                               'font_color': 'rgb(255,255,255)',
                               'font_size': 48}
        self._all_styles[16] = {'color': 'rgb(220,147,93)',
                               'font_color': 'rgb(255,255,255)',
                               'font_size': 48}
        self._all_styles[32] = {'color': 'rgb(231,129,104,)',
                               'font_color': 'rgb(255,255,255)',
                               'font_size': 48}
        self._all_styles[64] = {'color': 'rgb(216,99,64)',
                               'font_color': 'rgb(255,255,255)',
                               'font_size': 48}
        self._all_styles[128] = {'color': 'rgb(239,217,123)',
                               'font_color': 'rgb(255,255,255)',
                               'font_size': 48}
        self._all_styles[256] = {'color': 'rgb(236,209,99)',
                               'font_color': 'rgb(255,255,255)',
                               'font_size': 48}
        self._all_styles[512] = {'color': 'rgb(225,191,76)',
                               'font_color': 'rgb(255,255,255)',
                               'font_size': 48}
        self._all_styles[1024] = {'color': 'rgb(221,186,66)',
                               'font_color': 'rgb(255,255,255)',
                               'font_size': 48}
        self._all_styles[2048] = {'color': 'rgb(230,97,66)',
                               'font_color': 'rgb(255,255,255)',
                               'font_size': 48}
        self._all_styles[4096] = {'color': 'rgb(236,228,219)',
                               'font_color': 'rgb(255,255,255)',
                               'font_size': 48}


        self.value = value
        self.remap()
        self.show()


    @property
    def value(self):
        if self._value == '':
            return 0
        return self._value

    @value.setter
    def value(self, value):
        self._value = value
        self.setStyleSheet(self.default_style.format(**self._all_styles[value]))
        if value == 0:
            value = ''
        self._value_label.setText(str(value))

    @property
    def length(self):
        return self.width()

    @length.setter
    def length(self, new_size):
        self.resize(new_size, new_size)
        self.remap()

    @property
    def location(self):
        loc = self.geometry()
        loc: QtCore.QRect
        return (loc.x(),loc.y())

    @location.setter
    def location(self, pos):
        self.move(pos[0],pos[1])

    def remap(self):
        spacing = self.width() - 24 +  1.4 * self._game_size + 26/5
        self.location = (spacing * self._pos[1],
                        (spacing * self._pos[0]))
