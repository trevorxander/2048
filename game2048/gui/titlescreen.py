# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'titlescreen.ui'
#
# Created by: PyQt5 UI code generator 5.10.1
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_titlescreen(object):
    def setupUi(self, titlescreen):
        titlescreen.setObjectName("titlescreen")
        titlescreen.resize(430, 568)
        self.verticalLayout = QtWidgets.QVBoxLayout(titlescreen)
        self.verticalLayout.setObjectName("verticalLayout")
        self.game_options = QtWidgets.QVBoxLayout()
        self.game_options.setSpacing(0)
        self.game_options.setObjectName("game_options")
        self.single_player = Button(titlescreen)
        self.single_player.setObjectName("single_player")
        self.game_options.addWidget(self.single_player)
        self.single_player_options = QtWidgets.QHBoxLayout()
        self.single_player_options.setObjectName("single_player_options")
        self.solo = Button(titlescreen)
        self.solo.setObjectName("solo")
        self.single_player_options.addWidget(self.solo)
        self.computer = Button(titlescreen)
        self.computer.setObjectName("computer")
        self.single_player_options.addWidget(self.computer)
        self.game_options.addLayout(self.single_player_options)
        self.computer_options = QtWidgets.QHBoxLayout()
        self.computer_options.setObjectName("computer_options")
        self.easy = Button(titlescreen)
        self.easy.setObjectName("easy")
        self.computer_options.addWidget(self.easy)
        self.medium = Button(titlescreen)
        self.medium.setObjectName("medium")
        self.computer_options.addWidget(self.medium)
        self.hard = Button(titlescreen)
        self.hard.setObjectName("hard")
        self.computer_options.addWidget(self.hard)
        self.game_options.addLayout(self.computer_options)
        self.two_player = Button(titlescreen)
        self.two_player.setObjectName("two_player")
        self.game_options.addWidget(self.two_player)
        self.game_options.setStretch(0, 1)
        self.game_options.setStretch(1, 1)
        self.game_options.setStretch(2, 1)
        self.game_options.setStretch(3, 1)
        self.verticalLayout.addLayout(self.game_options)

        self.retranslateUi(titlescreen)
        QtCore.QMetaObject.connectSlotsByName(titlescreen)

    def retranslateUi(self, titlescreen):
        _translate = QtCore.QCoreApplication.translate
        titlescreen.setWindowTitle(_translate("titlescreen", "Form"))

from game2048.gui.elements import Button
