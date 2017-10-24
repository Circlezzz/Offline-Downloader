#!/usr/bin/env python3
#-*- coding:utf-8 -*-

from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *


class retriveDlg(QDialog):
    def __init__(self, parent):
        super().__init__(parent)

        self.InitUI()

    def InitUI(self):
        mainlayout = QGridLayout(self)
        self.setLayout = mainlayout
        PathLabel = QLabel('Save Path', self)
        ThreadLabel = QLabel('Thread Num', self)
        self.PathLineEdit = QLineEdit(self)
        self.ThreadSpinbox = QSpinBox(self)
        self.ThreadSpinbox.setRange(1, 20)
        getDirBtn = QPushButton('Open', self)
        self.OkBtn = QPushButton('Ok', self)
        CancelBtn = QPushButton('Cancel', self)
        mainlayout.addWidget(PathLabel, 1, 0)
        mainlayout.addWidget(self.PathLineEdit, 1, 1)
        mainlayout.addWidget(getDirBtn, 1, 2)
        mainlayout.addWidget(ThreadLabel, 2, 0)
        middlelayout = QHBoxLayout()
        middlelayout.addWidget(self.ThreadSpinbox)
        middlelayout.addStretch()
        mainlayout.addLayout(middlelayout, 2, 1)

        downlayout = QHBoxLayout()
        downlayout.addStretch()
        downlayout.addWidget(self.OkBtn)
        downlayout.addWidget(CancelBtn)
        mainlayout.addLayout(downlayout, 3, 1)
        self.setFixedSize(520, 155)
        self.setWindowTitle('Retrieve to local')
        self.setWindowIcon(QIcon('./res/icon.png'))

        getDirBtn.clicked.connect(self.GetDir)
        CancelBtn.clicked.connect(self.CancelPressed)

    def GetDir(self):
        path = QFileDialog.getExistingDirectory(
            self, 'Open a dir', '.',
            QFileDialog.ShowDirsOnly | QFileDialog.DontResolveSymlinks)
        self.PathLineEdit.setText(path)

    # def OkPressed(self):
    #     self.close()
    #     return self.PathLineEdit.text()

    def CancelPressed(self):
        self.close()
