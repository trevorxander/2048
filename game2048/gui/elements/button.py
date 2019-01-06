from PyQt5 import QtCore, QtGui, QtWidgets


class Button(QtWidgets.QWidget):
    def __init__(self, parent=None, text=''):
        QtWidgets.QWidget.__init__(self, parent=parent)
        self.ui = ButtonUI()
        self.ui.setupUi(self)

        self.button = self.ui.pushButton

        self.released = self.button.released
        self.set_text(text)

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


class ButtonUI(object):
    def setupUi(self, Button):
        Button.setObjectName("Button")
        Button.resize(226, 123)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(Button.sizePolicy().hasHeightForWidth())
        Button.setSizePolicy(sizePolicy)
        Button.setMinimumSize(QtCore.QSize(0, 63))
        Button.setMaximumSize(QtCore.QSize(280, 16777215))
        Button.setCursor(QtGui.QCursor(QtCore.Qt.OpenHandCursor))
        self.gridLayout = QtWidgets.QGridLayout(Button)
        self.gridLayout.setObjectName("gridLayout")
        self.pushButton = QtWidgets.QPushButton(Button)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.MinimumExpanding, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.pushButton.sizePolicy().hasHeightForWidth())
        self.pushButton.setSizePolicy(sizePolicy)
        self.pushButton.setMinimumSize(QtCore.QSize(0, 50))
        self.pushButton.setCursor(QtGui.QCursor(QtCore.Qt.OpenHandCursor))
        self.pushButton.setFlat(False)
        self.pushButton.setObjectName("pushButton")
        self.gridLayout.addWidget(self.pushButton, 0, 0, 1, 1)

        QtCore.QMetaObject.connectSlotsByName(Button)
