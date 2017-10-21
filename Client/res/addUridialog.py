#!/usr/bin/env python3
#-*- coding:utf-8 -*-

from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from res.Sendcmd import SendCommand


class addUridlg(QDialog):
    def __init__(self, parent):
        super().__init__(parent)

        self.InitUI()

    def InitUI(self):
        mainlayout = QGridLayout(self)
        self.setLayout = mainlayout
        UriLabel = QLabel('Uri', self)
        self.UriLineEdit = QLineEdit(self)
        self.UriLineEdit.setPlaceholderText(
            'Uri or Magnet link, splite with a space')
        self.OkBtn = QPushButton('Ok', self)
        CancelBtn = QPushButton('Cancel', self)
        mainlayout.addWidget(UriLabel, 0, 0)
        mainlayout.addWidget(self.UriLineEdit, 0, 1)

        downlayout = QHBoxLayout()
        downlayout.addWidget(self.OkBtn)
        downlayout.addWidget(CancelBtn)
        downlayout.addStretch()
        mainlayout.addLayout(downlayout, 1, 1)
        self.setFixedSize(520, 100)

        # OkBtn.clicked.connect(self.OkPressed)
        CancelBtn.clicked.connect(self.CancelPressed)

    def CancelPressed(self):
        self.close()
