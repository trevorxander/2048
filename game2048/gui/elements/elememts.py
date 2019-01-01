from PyQt5 import QtCore, QtGui, QtWidgets, uic

class Label (QtWidgets.QWidget):
    def __init__(self, parent = None, Label='test', val = 0):
        QtWidgets.QWidget.__init__(self, parent = parent)
        ui = uic.loadUi('../game2048/gui/elements/label.ui', self)
        label = ui.label
        label: QtWidgets.QLabel

        label = ui.value
        label: QtWidgets.QLabel

        self.show()

class Button (QtWidgets.QWidget):
    def __init__(self, parent = None, text=''):
        QtWidgets.QWidget.__init__(self, parent = parent)
        ui = uic.loadUi('../game2048/gui/elements/button.ui', self)

        self.show()

class Tile (QtWidgets.QWidget):
    def __init__(self, parent = None, value=0, pos = (0,0)):
        self.parent = parent
        self._pos = pos
        self._value = value
        QtWidgets.QWidget.__init__(self, parent = parent)
        ui = uic.loadUi('../game2048/gui/elements/tile.ui', self)
        self._value_label = ui.value_label

        self.format_text = '<html><head/><body><p align="center"><span style=" font-size:48pt;">{0}</span></p></body></html>'
        self.value = value
        self._map_from_pos(150, 140)
        self.show()


    @property
    def value(self):
        if self._value == '':
            return 0
        return self._value

    @value.setter
    def value(self, value):
        if value == 0:
            value = ''
        self._value_label.setText(self.format_text.format(value))

    @property
    def location(self):
        loc = self.geometry()
        loc: QtCore.QRect
        return (loc.x(),loc.y())

    @location.setter
    def location(self, pos):
        self.move(pos[0],pos[1])

    def _map_from_pos(self, horizontal, vertical):
        self.location = (horizontal * self._pos[1],
                        (vertical * self._pos[0]))
