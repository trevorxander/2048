from PyQt5 import QtCore, QtGui, QtWidgets


class Label(QtWidgets.QWidget):
    _LABEL_COLOR = 'rgb(185,173,162)'
    _DEFAULT_STYLE = '* {{ background-color: {color};' \
                    'border: 1px solid {color};' \
                    'border-radius: 10px;}}'

    def __init__(self, parent=None, label='Label', val=0):
        QtWidgets.QWidget.__init__(self, parent=parent)

        self._ui = LabelUI()
        self._ui.setupUi(self)
        self._label = self._ui.label
        self._value = self._ui.value

        self.setStyleSheet(self._DEFAULT_STYLE.format(color=self._LABEL_COLOR))
        self.set_label(label)
        self.set_value(val)
        self.show()

    def set_label(self, label):
        self._label.setText(str(label))

    def set_value(self, value):
        self._value.setText(str(value))



class LabelUI(object):
    def setupUi(self, Label):
        Label.setObjectName("Label")
        Label.resize(280, 96)
        Label.setMinimumSize(QtCore.QSize(0, 96))
        Label.setMaximumSize(QtCore.QSize(280, 96))
        self.gridLayout_2 = QtWidgets.QGridLayout(Label)
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.frame = QtWidgets.QFrame(Label)
        self.frame.setFrameShape(QtWidgets.QFrame.Box)
        self.frame.setFrameShadow(QtWidgets.QFrame.Plain)
        self.frame.setObjectName("frame")
        self.gridLayout = QtWidgets.QGridLayout(self.frame)
        self.gridLayout.setObjectName("gridLayout")
        self.verticalLayout = QtWidgets.QVBoxLayout()
        self.verticalLayout.setSizeConstraint(QtWidgets.QLayout.SetMinAndMaxSize)
        self.verticalLayout.setSpacing(0)
        self.verticalLayout.setObjectName("verticalLayout")
        self.label = QtWidgets.QLabel(self.frame)
        self.label.setMinimumSize(QtCore.QSize(0, 0))
        self.label.setMaximumSize(QtCore.QSize(16777215, 100))
        self.label.setObjectName("label")
        self._label_style = '* {{ color: {color};' \
                            'font-size: {font_size}px  }}'
        label_font_color = 'rgb(255,255,255)'
        value_font_size = 30
        label_font_size = 15
        self.label.setStyleSheet(self._label_style.format(color=label_font_color,
                                                          font_size=label_font_size))

        self.verticalLayout.addWidget(self.label, 0, QtCore.Qt.AlignHCenter | QtCore.Qt.AlignVCenter)
        self.value = QtWidgets.QLabel(self.frame)
        self.value.setMinimumSize(QtCore.QSize(0, 0))
        self.value.setMaximumSize(QtCore.QSize(16777215, 200))
        self.value.setObjectName("value")
        self.value.setStyleSheet(self._label_style.format(color=label_font_color,
                                                          font_size=value_font_size))
        self.verticalLayout.addWidget(self.value, 0, QtCore.Qt.AlignHCenter | QtCore.Qt.AlignVCenter)
        self.verticalLayout.setStretch(0, 1)
        self.verticalLayout.setStretch(1, 1)
        self.gridLayout.addLayout(self.verticalLayout, 0, 0, 1, 1)
        self.gridLayout_2.addWidget(self.frame, 0, 0, 1, 1)
