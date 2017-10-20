#!/usr/bin/env python3
#-*- coding:utf-8 -*-

from PyQt5.QtWidgets import *
from PyQt5.QtCore import *

class addUridlg(QDialog):
    def __init__(self):
        super().__init__()

        self.InitUI()
    
    def InitUI(self):
        mainlayout=QGridLayout(self)
        self.setLayout=mainlayout
        UriLabel=QLabel('Uri',self)
        PathLabel=QLabel('Save Path',self)