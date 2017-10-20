#!/usr/bin/env python3
#-*- coding:utf-8 -*-

from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
import json

class loginWidget(QDialog):
    def __init__(self,parent):
        super().__init__(parent)

        self.InitUI()

    def InitUI(self):
        layout=QGridLayout(self)
        self.setLayout(layout)
        self.UsernameLabel=QLabel('Username',self)
        self.PasswdLabel=QLabel('Password',self)
        self.IPLabel=QLabel('Server IP',self)
        self.portLabel=QLabel('Server port',self)
        self.UsernameLineEdit=QLineEdit(self)
        self.PasswdLineEdit=QLineEdit(self)
        self.PasswdLineEdit.setEchoMode(QLineEdit.PasswordEchoOnEdit)
        self.IPLineEdit=QLineEdit(self)
        self.portLineEdit=QLineEdit(self)
        self.ApplyBtn=QPushButton('Apply')
        self.CancelBtn=QPushButton('Cancel')
        layout.addWidget(self.IPLabel,0,0)
        layout.addWidget(self.portLabel,1,0)
        layout.addWidget(self.UsernameLabel,2,0)
        layout.addWidget(self.PasswdLabel,3,0)
        layout.addWidget(self.IPLineEdit,0,1)
        layout.addWidget(self.portLineEdit,1,1)
        layout.addWidget(self.UsernameLineEdit,2,1)
        layout.addWidget(self.PasswdLineEdit,3,1)
        layout.addWidget(self.ApplyBtn,5,0)
        layout.addWidget(self.CancelBtn,5,1)
        self.setFixedSize(240,180)
        self.CancelBtn.clicked.connect(self.quit)
    
    def quit(self):
        self.close()


