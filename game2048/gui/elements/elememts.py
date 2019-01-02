from PyQt5 import QtCore, QtGui, QtWidgets, uic

class Label (QtWidgets.QWidget):
    def __init__(self, parent = None, Label='test', val = 0):
        QtWidgets.QWidget.__init__(self, parent = parent)
        self.ui = uic.loadUi('../game2048/gui/elements/label.ui', self)

        self._label = self.ui.label

        self._value = self.ui.value

        self.show()

    def set_label(self, label):
        self._label.setText(label)


    def set_value(self, value):
        self._value.setText(value)


class Button (QtWidgets.QWidget):
    def __init__(self, parent = None, text=''):
        QtWidgets.QWidget.__init__(self, parent = parent)
        ui = uic.loadUi('../game2048/gui/elements/button.ui', self)

        self.show()

class Tile (QtWidgets.QWidget):
    GRID_SPACING = 10
    def __init__(self, parent = None, value=0, pos = (0,0)):
        self.parent = parent
        self._pos = pos
        self._value = value
        QtWidgets.QWidget.__init__(self, parent = parent)
        ui = uic.loadUi('../game2048/gui/elements/tile.ui', self)
        self._value_label = ui.value_label

        self.format_text = '<html><head/><body><p align="center"><span style=" font-size:48pt;">{0}</span></p></body></html>'
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
        if value == 0:
            value = ''
        self._value_label.setText(self.format_text.format(value))

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
        spacing = self.width() - 24 + Tile.GRID_SPACING
        self.location = (spacing * self._pos[1],
                        (spacing * self._pos[0]))
