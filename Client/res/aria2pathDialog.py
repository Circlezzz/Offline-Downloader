#!/usr/bin/env python3
#-*- coding:utf-8 -*-

from PyQt5.QtWidgets import *
from PyQt5.QtCore import *


class ariapathDlg(QDialog):
    def __init__(self, parent):
        super().__init__(parent)

        self.InitUI()

    def InitUI(self):
        mainlayout = QGridLayout(self)
        exepathLabel = QLabel('aria2 Path')
        confpathLabel = QLabel('aria2 configure file path')
        self.exepathLineEdit = QLineEdit(self)
        self.exepathLineEdit.setFocusPolicy(Qt.NoFocus)
        self.confpathLineEdit = QLineEdit(self)
        self.confpathLineEdit.setFocusPolicy(Qt.NoFocus)
        exepathBtn = QPushButton('Open')
        confpathBtn = QPushButton('Open')
        self.okBtn = QPushButton('Ok')
        CancelBtn = QPushButton('Cancel')

        mainlayout.addWidget(exepathLabel, 0, 0)
        mainlayout.addWidget(self.exepathLineEdit, 0, 1)
        mainlayout.addWidget(exepathBtn, 0, 2)
        mainlayout.addWidget(confpathLabel, 1, 0)
        mainlayout.addWidget(self.confpathLineEdit, 1, 1)
        mainlayout.addWidget(confpathBtn, 1, 2)
        mainlayout.addWidget(self.okBtn, 2, 1)
        mainlayout.addWidget(CancelBtn, 2, 2)
        self.setWindowTitle('Path Settings')

        CancelBtn.clicked.connect(self.onCancelClicked)
        exepathBtn.clicked.connect(self.setEXEPath)
        confpathBtn.clicked.connect(self.setConfPath)

    def onCancelClicked(self):
        self.close()

    def setEXEPath(self):
        path = QFileDialog.getOpenFileName(self, 'Choose aria2 path', '.',
                                           'aria2(aria2c.exe)')
        self.exepathLineEdit.setText(path[0])

    def setConfPath(self):
        path = QFileDialog.getOpenFileName(
            self, 'Choose aria2 configure file path', '.',
            'aria2 configure file(aria2.conf)')
        self.confpathLineEdit.setText(path[0])