#!/usr/bin/env python3
#-*- coding:utf-8 -*-

from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
import sys
import res.Getfile
from res.addUridialog import addUridlg
from res.connectionSetup import loginWidget
from res.Getfile import openFtp
from res.retriveDialog import retriveDlg
import res.Sendcmd
import json
import os
from collections import OrderedDict


class Main(QMainWindow):
    def __init__(self):
        super().__init__()
        self.isConnected=False

        self.InitUI()

    def InitUI(self):
        mainwidget = QWidget(self)
        self.setCentralWidget(mainwidget)
        layout = QVBoxLayout(mainwidget)
        self.taskTable = QTableWidget(mainwidget)
        layout.addWidget(self.taskTable)
        self.taskTable.setColumnCount(6)
        self.taskTable.horizontalHeader().setStretchLastSection(True)
        self.taskTable.setSelectionBehavior(QAbstractItemView.SelectRows)
        header = ['File Name','Link Address' ,'Size', 'Offline Status','Offline Process', 'Download Process']
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
        self.Start_Server_Download = QAction('Start Offline Download',
                                        self.taskTable)
        self.Pause_Server_Download = QAction('Pause Offline Download',
                                        self.taskTable)
        self.Start_Local_Download = QAction('Start Retrieve', self.taskTable)
        self.Pause_Local_Download = QAction('Pause Retrieve', self.taskTable)
        self.Delete_Local_Download = QAction('Delete From List', self.taskTable)
        self.Delete_Server_Download = QAction('Delete From Server', self.taskTable)
        self.popMenu.addAction(self.Start_Server_Download)
        self.popMenu.addAction(self.Pause_Server_Download)
        self.popMenu.addAction(self.Start_Local_Download)
        self.popMenu.addAction(self.Pause_Local_Download)
        self.popMenu.addAction(self.Delete_Server_Download)
        self.popMenu.addAction(self.Delete_Local_Download)
        self.Start_Server_Download.triggered.connect(self.Start_Server_Download_slot)
        self.Pause_Server_Download.triggered.connect(self.Pause_Server_Download_slot)
        self.Delete_Server_Download.triggered.connect(self.Delete_Server_Download_slot)
        self.taskTable.customContextMenuRequested.connect(self.showMenu)

        self.retriveDlg=None
        self.Start_Local_Download.triggered.connect(self.showLocalDownloadDlg)

        menu = self.menuBar()
        SettingMenu = QMenu('&Setting', self)
        LoginAct = QAction('Login', self)
        SettingMenu.addAction(LoginAct)
        menu.addMenu(SettingMenu)
        TaskMenu = QMenu('&New Task', self)
        AddUriAct = QAction('Add Uri', self)
        AddtorrentAct = QAction('Add Torrent', self)
        TaskMenu.addActions([AddUriAct, AddtorrentAct])
        menu.addMenu(TaskMenu)
        AboutMenu = QMenu('&About', self)
        AboutAct = QAction('About', self)
        AboutQtAct = QAction('About Qt', self)
        AboutMenu.addActions([AboutAct, AboutQtAct])
        menu.addMenu(AboutMenu)

        self.LoginWidget = None
        self.AddUridlg = None
        self.AddTorrentdlg = None
        LoginAct.triggered.connect(self.showLogindlg)
        AddUriAct.triggered.connect(self.showAddUridlg)
        AddtorrentAct.triggered.connect(self.showAddTorrentdlg)
        AboutAct.triggered.connect(self.showAboutmedlg)
        AboutQtAct.triggered.connect(self.showAboutQtdlg)

        self.ftp = None
        self.userinfo = None
        self.filesInfo=OrderedDict()
        self.timer=None
        if os.path.exists('./res/fileInfo.json'):
            with open('./res/fileInfo.json') as file:
                self.filesInfo = json.load(file)            
        if os.path.exists('./res/serverInfo.json'):
            with open('./res/serverInfo.json') as file:
                self.userinfo = json.load(file)
            self.ip = self.userinfo['ip']
            self.passwd = self.userinfo['passwd']
            self.username = self.userinfo['username']
            self.port = int(self.userinfo['port'])
            self.login()
            self.getFileList(repaint=True)

    def showMenu(self, pos):
        for action in self.popMenu.actions():
            action.setEnabled(True)
        self.currentIndex = self.taskTable.indexAt(pos).row()
        if self.currentIndex <0:
            for action in self.popMenu.actions():
                action.setEnabled(False)
            
        self.popMenu.exec_(QCursor.pos())

    def showLogindlg(self):
        if not self.LoginWidget:
            self.LoginWidget = loginWidget(self)
            self.LoginWidget.setModal(True)
            self.LoginWidget.ApplyBtn.clicked.connect(self.login)
        if self.userinfo:
            self.LoginWidget.IPLineEdit.setText(self.userinfo['ip'])
            self.LoginWidget.portLineEdit.setText(str(self.userinfo['port']))
            self.LoginWidget.UsernameLineEdit.setText(
                self.userinfo['username'])
            self.LoginWidget.PasswdLineEdit.setText(self.userinfo['passwd'])
        self.LoginWidget.show()
        self.ip = self.LoginWidget.IPLineEdit.text()
        self.passwd = self.LoginWidget.PasswdLineEdit.text()
        self.username = self.LoginWidget.UsernameLineEdit.text()
        self.port = int(self.LoginWidget.portLineEdit.text())

    def login(self):
        try:
            #print(self.ip,self.port,self.username,self.passwd)
            self.ftp = openFtp(self.ip, self.port, self.username, self.passwd)
            self.getFileList(repaint=True)
        except OSError:
            QMessageBox.critical(self.LoginWidget, 'Error', 'connection faild')
        else:
            if self.LoginWidget:
                self.LoginWidget.close()
            with open('./res/serverInfo.json', 'w+') as file:
                json.dump({
                    'ip': self.ip,
                    'port': self.port,
                    'username': self.username,
                    'passwd': self.passwd
                }, file)
            self.timer=QTimer(self)
            self.timer.timeout.connect(self.getFileList)
            self.timer.start(3000)

    def getFileList(self,repaint=False):
        if repaint:
            self.taskTable.clearContents()
            for i in range(self.taskTable.rowCount()):
                self.taskTable.removeRow(i)
        if self.ftp:
            for i,gid in enumerate(self.filesInfo.keys()):
                # print(gid)
                r=res.Sendcmd.SendCommand('getFiles '+gid,res.Sendcmd.server,res.Sendcmd.port)
                status=json.loads(r)
                # print(status)
                if repaint:
                    linkitm=QTableWidgetItem(status['result'][0]['uris'][0]['uri'])
                    nameitm = QTableWidgetItem(status['result'][0]['path'])
                    sizeitm = QTableWidgetItem(status['result'][0]['length'])
                    statusitem = QTableWidgetItem(status['result'][0]['uris'][1]['status'])
                    OfflineProcess=QTableWidgetItem(status['result'][0]['completedLength']+'/'+status['result'][0]['length'])
                    self.taskTable.insertRow(i)
                    self.taskTable.setItem(i, 0, nameitm)
                    self.taskTable.setItem(i,1,linkitm)
                    self.taskTable.setItem(i, 2, sizeitm)
                    self.taskTable.setItem(i, 3, statusitem)
                    self.taskTable.setItem(i,4,OfflineProcess)
                    self.taskTable.setCellWidget(i, 5, QProgressBar(self.taskTable))
                else:
                    self.taskTable.item(i,1).setText(status['result'][0]['uris'][0]['uri'])
                    self.taskTable.item(i,0).setText(status['result'][0]['path'])
                    self.taskTable.item(i,2).setText(status['result'][0]['length'])
                    self.taskTable.item(i,3).setText(status['result'][0]['uris'][1]['status'])
                    self.taskTable.item(i,4).setText(status['result'][0]['completedLength']+'/'+status['result'][0]['length'])
                    self.filesInfo[gid]=status['result'][0]['path']

                

    def showAddUridlg(self):
        if not self.AddUridlg:
            self.AddUridlg = addUridlg(self)
            self.AddUridlg.OkBtn.clicked.connect(self.AddNewUri)
            self.AddUridlg.setModal(True)
        self.AddUridlg.show()

    def AddNewUri(self):
        data=res.Sendcmd.SendCommand('addUri '+self.AddUridlg.UriLineEdit.text(),res.Sendcmd.server,res.Sendcmd.port)
        print(data)
        j=json.loads(data)
        print(j)
        gid=j['result']
        print(gid)
        data=res.Sendcmd.SendCommand('getFiles '+gid,res.Sendcmd.server,res.Sendcmd.port)
        print(data)
        j=json.loads(data)
        filename=j['result'][0]['path'].split('/')[-1]
        self.filesInfo.update({gid:filename})
        with open('res/fileInfo.json','w+') as file:
            json.dump(self.filesInfo,file)
        self.AddUridlg.close()
        self.getFileList(repaint=True)

    def showAddTorrentdlg(self):
        pass

    def showAboutmedlg(self):
        pass

    def showAboutQtdlg(self):
        QMessageBox.aboutQt(self, 'About Qt')

    def showLocalDownloadDlg(self):
        if not self.retriveDlg:
            self.retriveDlg=retriveDlg(self)
            self.retriveDlg.setModal(True)
            self.retriveDlg.OkBtn.clicked.connect(self.getLocalPath)
        self.retriveDlg.show()

    def getLocalPath(self):
        LocalPath=self.retriveDlg.PathLineEdit.text()
        if not LocalPath or not os.path.exists(LocalPath):
            QMessageBox.critical(self,'Invalid Path','Invalid Path')
        else:
            pass

    def Start_Server_Download_slot(self):
        gid=self.filesInfo.keys()[self.currentIndex]
        res.Sendcmd.SendCommand('unpause '+gid,res.Sendcmd.server,res.Sendcmd.port)

    def Pause_Server_Download_slot(self):
        gid=self.filesInfo.keys()[self.currentIndex]
        res.Sendcmd.SendCommand('pause '+gid,res.Sendcmd.server,res.Sendcmd.port)

    def Delete_Server_Download_slot(self):
        gid=self.filesInfo.keys()[self.currentIndex]
        res.Sendcmd.SendCommand('remove '+gid,res.Sendcmd.server,res.Sendcmd.port)
        res.Sendcmd.SendCommand('removeDownloadResult '+gid,res.Sendcmd.server,res.Sendcmd.port)
        res.Sendcmd.SendCommand('_delLocalFile_ '+self.filesInfo[gid],res.Sendcmd.server,res.Sendcmd.port)
        del self.filesInfo[gid]
        self.taskTable.removeRow(self.currentIndex)


    def closeEvent(self,event):
        if os.path.exists('./res/fileInfo.json'):
            if len(self.filesInfo):
                with open('./res/fileInfo.json','w') as file:
                    json.dump(self.filesInfo,file)
            else:
                os.remove('./res/fileInfo.json')
        event.accept()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    mainwindow = Main()
    mainwindow.show()
    sys.exit(app.exec_())