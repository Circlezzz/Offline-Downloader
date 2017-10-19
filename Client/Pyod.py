#!/usr/bin/env python3
#-*- coding:utf-8 -*-

from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
import sys
import res.Getfile
from res.connectionSetup import loginWidget
from res.Getfile import openFtp
import json
import os


class Main(QMainWindow):
    def __init__(self):
        super().__init__()

        self.InitUI()

    def InitUI(self):
        mainwidget = QWidget(self)
        self.setCentralWidget(mainwidget)
        layout = QVBoxLayout(mainwidget)
        self.taskTable = QTableWidget(mainwidget)
        layout.addWidget(self.taskTable)
        self.taskTable.setColumnCount(4)
        self.taskTable.horizontalHeader().setStretchLastSection(True)
        self.taskTable.setSelectionBehavior(QAbstractItemView.SelectRows)
        header = ['File Name', 'Size', 'Offline Status', 'Download Process']
        self.taskTable.setHorizontalHeaderLabels(header)
        self.taskTable.setMinimumSize(1000, 600)
        self.taskTable.setColumnWidth(0, 300)
        self.taskTable.setColumnWidth(1, 150)
        self.taskTable.setColumnWidth(2, 150)
        self.taskTable.setFrameShape(QFrame.NoFrame)
        self.taskTable.verticalHeader().hide()
        self.taskTable.setShowGrid(False)
        self.taskTable.setMouseTracking(True)
        self.taskTable.setEditTriggers(QAbstractItemView.NoEditTriggers)

        self.taskTable.setContextMenuPolicy(Qt.CustomContextMenu)
        self.popMenu = QMenu(self.taskTable)
        Start_Server_Download = QAction('Start Offline Download', self.taskTable)
        Pause_Server_Download = QAction('Pause Offline Download', self.taskTable)
        Start_Local_Download=QAction('Start Retrieve',self.taskTable)
        Pause_Local_Download=QAction('Pause Retrieve',self.taskTable)
        Delete_Local_Download=QAction('Delete From List',self.taskTable)
        Delete_Server_Download = QAction('Delete From Server', self.taskTable)
        self.popMenu.addAction(Start_Server_Download)
        self.popMenu.addAction(Pause_Server_Download)
        self.popMenu.addAction(Start_Local_Download)
        self.popMenu.addAction(Pause_Local_Download)
        self.popMenu.addAction(Delete_Server_Download)
        self.popMenu.addAction(Delete_Local_Download)
        self.taskTable.customContextMenuRequested.connect(self.showMenu)

        menu=self.menuBar()
        SettingMenu=QMenu('&Setting',self)
        LoginAct=QAction('Login',self)
        SettingMenu.addAction(LoginAct)
        menu.addMenu(SettingMenu)
        TaskMenu=QMenu('&New Task',self)
        AddUriAct=QAction('Add Uri',self)
        AddtorrentAct=QAction('Add Torrent',self)
        TaskMenu.addActions([AddUriAct,AddtorrentAct])
        menu.addMenu(TaskMenu)
        AboutMenu=QMenu('&About',self)
        AboutAct=QAction('About',self)
        AboutMenu.addAction(AboutAct)
        menu.addMenu(AboutMenu)

        self.LoginWidget=None
        LoginAct.triggered.connect(self.showLoginWidget)

        self.ftp=None
        self.userinfo=None
        if os.path.exists('./res/serverInfo.json'):
            with open('./res/serverInfo.json') as file:
                self.userinfo=json.load(file)

    def showMenu(self, pos):
        self.currentIndex = self.taskTable.indexAt(pos).row()
        self.popMenu.exec_(QCursor.pos())
    
    def showLoginWidget(self):
        if not self.LoginWidget:
            self.LoginWidget=loginWidget()
            self.LoginWidget.setWindowModality(Qt.ApplicationModal)
            self.LoginWidget.ApplyBtn.clicked.connect(self.login)
        if self.userinfo:
            self.LoginWidget.IPLineEdit.setText(self.userinfo['ip'])
            self.LoginWidget.portLineEdit.setText(str(self.userinfo['port']))
            self.LoginWidget.UsernameLineEdit.setText(self.userinfo['username'])
            self.LoginWidget.PasswdLineEdit.setText(self.userinfo['passwd'])
        self.LoginWidget.show()

    def login(self):
        self.ip=self.LoginWidget.IPLineEdit.text()
        self.passwd=self.LoginWidget.PasswdLineEdit.text()
        self.username=self.LoginWidget.UsernameLineEdit.text()
        self.port=int(self.LoginWidget.portLineEdit.text())
        try:
            #print(self.ip,self.port,self.username,self.passwd)
            self.ftp=openFtp(self.ip,self.port,self.username,self.passwd)
            self.getFileList()
        except OSError:
            QMessageBox.critical(self.LoginWidget,'Error','connection faild')
        else:
            self.LoginWidget.close()
            with open('./res/serverInfo.json','w+') as file:
                json.dump({'ip':self.ip,'port':self.port,'username':self.username,'passwd':self.passwd},file)


    def getFileList(self):
        if self.ftp:
            self.fileList=self.ftp.nlst()
            for i,name in enumerate(self.fileList):
                self.taskTable.insertRow(i)
                self.ftp.voidcmd('TYPE I')
                nameitm=QTableWidgetItem(name)
                sizeitm=QTableWidgetItem(str(self.ftp.size(name)))
                statusitem=QTableWidgetItem('Done')
                self.taskTable.setItem(i,0,nameitm)
                self.taskTable.setItem(i,1,sizeitm)
                self.taskTable.setItem(i,2,statusitem)
                self.taskTable.setCellWidget(i,3,QProgressBar(self.taskTable))


if __name__ == '__main__':
    app = QApplication(sys.argv)
    mainwindow = Main()
    mainwindow.show()
    sys.exit(app.exec_())