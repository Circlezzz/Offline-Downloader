#!/usr/bin/env python3
#-*- coding:utf-8 -*-

from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
import sys
import res.Getfile
from res.connectionSetup import loginWidget
from res.Getfile import openFtp


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
        header = ['File Name', 'Size', 'Status', 'Download Process']
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
        StartDownload = QAction('Start', self.taskTable)
        PauseDownload = QAction('Pause', self.taskTable)
        DeleteDownload = QAction('Delete', self.taskTable)
        self.popMenu.addAction(StartDownload)
        self.popMenu.addAction(PauseDownload)
        self.popMenu.addAction(DeleteDownload)
        self.taskTable.customContextMenuRequested.connect(self.showMenu)

        menu=self.menuBar()
        SettingMenu=QMenu('Setting',self)
        LoginAct=QAction('Login',self)
        SettingMenu.addAction(LoginAct)
        menu.addMenu(SettingMenu)
        self.LoginWidget=None
        LoginAct.triggered.connect(self.showLoginWidget)

        self.ftp=None

    def showMenu(self, pos):
        self.currentIndex = self.taskTable.indexAt(pos).row()
        self.popMenu.exec_(QCursor.pos())
    
    def showLoginWidget(self):
        if self.LoginWidget:
            self.LoginWidget.show()
        else:
            self.LoginWidget=loginWidget()
            self.LoginWidget.ApplyBtn.clicked.connect(self.login)
            self.LoginWidget.show()

    def login(self):
        self.ip=self.LoginWidget.IPLineEdit.text()
        self.passwd=self.LoginWidget.PasswdLineEdit.text()
        self.username=self.LoginWidget.UsernameLineEdit.text()
        self.port=int(self.LoginWidget.portLineEdit.text())
        try:
            self.ftp=openFtp(self.ip,self.port,self.username,self.passwd)
            self.getFileList()
        except OSError:
            QMessageBox.critical(self.LoginWidget,'Error','connection faild')


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