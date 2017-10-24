#!/usr/bin/env python3
#-*- coding:utf-8 -*-

from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *


class aboutmedialog(QDialog):
    def __init__(self, parent):
        super().__init__(parent)

        self.InitUI()

    def InitUI(self):
        layout = QVBoxLayout(self)
        titleLabel = QLabel('Python Offline Downloader')
        iconLabel = QLabel()
        iconLabel.setMaximumSize(200, 200)
        iconLabel.setPixmap(QPixmap('./res/icon.png').scaled(200, 200))
        dataLabel = QLabel('2017.10.24')
        layout.addWidget(titleLabel)
        layout.addWidget(iconLabel)
        layout.addWidget(dataLabel)
        self.setWindowTitle('About me')