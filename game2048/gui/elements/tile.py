from PyQt5 import QtCore, QtGui, QtWidgets


class Tile(QtWidgets.QWidget):
    _GRID_SPACING = 16
    _LABEL_STYLE = 'QLabel {{background-color: {color};' \
                   'color: {font_color};' \
                   'font-size: {font_size}px;' \
                   'border: 1px solid {color};' \
                   'font-weight: bold;' \
                   'border-radius: {border_radius};}}'

    def __init__(self, parent=None, value=0, pos=(0, 0)):
        QtWidgets.QWidget.__init__(self, parent=parent)

        self._parent = parent
        self._game_size = parent.parent()._grid_size
        self._pos = pos
        self._value = value
        ui = TileUI()
        ui.setupUi(self)

        self._value_label = ui.value_label

        self._max_tile_value = 4096
        self._value_label.setAlignment(QtCore.Qt.AlignCenter)

        self.value = value
        self._remap_to_grid()
        self.show()

    @property
    def value(self):
        if self._value == '':
            return 0
        return self._value

    @value.setter
    def value(self, tile_num):
        self._value = tile_num

        self.setStyleSheet(self.get_style('default'))
        if tile_num == 0:
            tile_num = ''
        self._value_label.setText(str(tile_num))

    @property
    def length(self):
        return self.width()

    @length.setter
    def length(self, new_size):
        self.resize(new_size, new_size)
        self._remap_to_grid()

    @property
    def location(self):
        loc = self.geometry()
        loc: QtCore.QRect
        return (loc.x(), loc.y())

    @location.setter
    def location(self, pos):
        self.move(pos[0], pos[1])

    def _remap_to_grid(self):
        spacing = self.width() - 24 + 1.3 * self._game_size + 26 / 5
        self.location = (spacing * self._pos[1],
                         (spacing * self._pos[0]))

    DEFAULT_TILE_THEME = {
            0: {'color': 'rgb(200,193,181)', 'font_color': 'rgb(0,0,0)', 'font_size': 48},
            2: {'color': 'rgb(236,228,219)', 'font_color': 'rgb(115,107,100)', 'font_size': 48},
            4: {'color': 'rgb(234,224,202)', 'font_color': 'rgb(115,107,100)', 'font_size': 48},
            8: {'color': 'rgb(232,179,129)', 'font_color': 'rgb(255,255,255)', 'font_size': 48},
            16: {'color': 'rgb(220,147,93)', 'font_color': 'rgb(255,255,255)', 'font_size': 48},
            32: {'color': 'rgb(231,129,104)', 'font_color': 'rgb(255,255,255)', 'font_size': 48},
            64: {'color': 'rgb(216,99,64)', 'font_color': 'rgb(255,255,255)', 'font_size': 48},
            128: {'color': 'rgb(239,217,123)', 'font_color': 'rgb(255,255,255)', 'font_size': 44},
            256: {'color': 'rgb(236,209,99)', 'font_color': 'rgb(255,255,255)', 'font_size': 43},
            512: {'color': 'rgb(225,191,76)', 'font_color': 'rgb(255,255,255)', 'font_size': 43},
            1024: {'color': 'rgb(221,186,66)', 'font_color': 'rgb(255,255,255)', 'font_size': 32},
            2048: {'color': 'rgb(230,97,66)', 'font_color': 'rgb(255,255,255)', 'font_size': 32},
            4096: {'color': 'rgb(236,228,219)', 'font_color': 'rgb(255,255,255)', 'font_size': 31}}

    THEME_MAP = {
            'default': DEFAULT_TILE_THEME
    }

    def get_style(self, name='default', border_radius='10px', **style):
        theme = self.THEME_MAP[name]
        largest_themed_tile = max(theme.keys())
        if self.value > largest_themed_tile:
            numbered_tile_theme = theme[largest_themed_tile]
        else:
            numbered_tile_theme = theme[self.value]
        tile_styling = self._LABEL_STYLE.format(border_radius=border_radius,
                                                **numbered_tile_theme,
                                                **style)
        return tile_styling


class TileUI(object):
    def setupUi(self, Tile):
        Tile.setObjectName("Tile")
        Tile.resize(140, 140)
        Tile.setMinimumSize(QtCore.QSize(70, 70))
        font = QtGui.QFont()
        font.setStyleStrategy(QtGui.QFont.PreferAntialias)
        Tile.setFont(font)
        self.horizontalLayout = QtWidgets.QHBoxLayout(Tile)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.value_label = QtWidgets.QLabel(Tile)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Ignored, QtWidgets.QSizePolicy.Ignored)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.value_label.sizePolicy().hasHeightForWidth())
        self.value_label.setSizePolicy(sizePolicy)
        self.value_label.setMinimumSize(QtCore.QSize(0, 0))
        font = QtGui.QFont()
        font.setStyleStrategy(QtGui.QFont.PreferAntialias)
        self.value_label.setFont(font)
        self.value_label.setFrameShape(QtWidgets.QFrame.Box)
        self.value_label.setFrameShadow(QtWidgets.QFrame.Plain)
        self.value_label.setLineWidth(0)
        self.value_label.setTextFormat(QtCore.Qt.RichText)
        self.value_label.setScaledContents(True)
        self.value_label.setObjectName("value_label")
        self.horizontalLayout.addWidget(self.value_label)
