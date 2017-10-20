#!/usr/bin/env python3
#-*- coding:utf-8 -*-

from PyQt5.QtWidgets import *
from PyQt5.QtCore import *

class addUridlg(QDialog):
    def __init__(self,parent):
        super().__init__(parent)

        self.InitUI()
    
    def InitUI(self):
        mainlayout=QGridLayout(self)
        self.setLayout=mainlayout
        UriLabel=QLabel('Uri',self)
        PathLabel=QLabel('Save Path',self)
        ThreadLabel=QLabel('Thread Num',self)
        UriLineEdit=QLineEdit(self)
        UriLineEdit.setPlaceholderText('Uri or Magnet link, splite with a space')
        PathLineEdit=QLineEdit(self)
        ThreadSpinbox=QSpinBox(self)
        ThreadSpinbox.setRange(1,20)
        getDirBtn=QPushButton('Open',self)
        OkBtn=QPushButton('Ok',self)
        CancelBtn=QPushButton('Cancel',self)