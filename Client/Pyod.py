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
import res.aria2pathDialog
import json
import os
from collections import OrderedDict
import subprocess
import signal

filesInfo = OrderedDict()
localFileInfo = list()


class Main(QMainWindow):
    def __init__(self):
        super().__init__()
        self.isConnected = False

        self.InitUI()

    def InitUI(self):
        mainwidget = QWidget(self)
        self.setCentralWidget(mainwidget)
        layout = QVBoxLayout(mainwidget)
        self.taskTable = QTableWidget(mainwidget)
        layout.addWidget(self.taskTable)
        self.taskTable.setColumnCount(10)
        self.taskTable.horizontalHeader().setStretchLastSection(True)
        self.taskTable.setSelectionBehavior(QAbstractItemView.SelectRows)
        header = [
            'File Name', 'Link Address', 'Size', 'Offline Status',
            'Offline Process', 'Offline Speed', 'Retrive Status',
            'Retrive Process', 'Retrive Speed', 'Save Path'
        ]
        self.taskTable.setHorizontalHeaderLabels(header)
        self.taskTable.setMinimumSize(1000, 600)
        # self.taskTable.setColumnWidth(0, 300)
        # self.taskTable.setColumnWidth(1, 150)
        # self.taskTable.setColumnWidth(2, 150)
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
        self.Resume_local_Download=QAction('Resume Retrieve',self.taskTable)
        self.Pause_Local_Download = QAction('Pause Retrieve', self.taskTable)
        self.Delete_Local_Download = QAction('Delete From List',
                                             self.taskTable)
        self.Delete_Server_Download = QAction('Delete From Server',
                                              self.taskTable)
        self.popMenu.addAction(self.Start_Server_Download)
        self.popMenu.addAction(self.Pause_Server_Download)
        self.popMenu.addAction(self.Delete_Server_Download)
        self.popMenu.addAction(self.Start_Local_Download)
        self.popMenu.addAction(self.Resume_local_Download)
        self.popMenu.addAction(self.Pause_Local_Download)
        self.popMenu.addAction(self.Delete_Local_Download)
        self.Start_Server_Download.triggered.connect(
            self.Start_Server_Download_slot)
        self.Pause_Server_Download.triggered.connect(
            self.Pause_Server_Download_slot)
        self.Delete_Server_Download.triggered.connect(
            self.Delete_Server_Download_slot)
        self.Resume_local_Download.triggered.connect(self.Resume_Retrieve_slot)
        self.Pause_Local_Download.triggered.connect(self.Pause_Retrieve_slot)
        self.Delete_Local_Download.triggered.connect(self.Delete_Retrieve_slot)
        self.taskTable.customContextMenuRequested.connect(self.showMenu)

        self.retriveDlg = None
        self.pathDlg = None
        self.Start_Local_Download.triggered.connect(self.showLocalDownloadDlg)

        menu = self.menuBar()
        SettingMenu = QMenu('&Setting', self)
        LoginAct = QAction('Login', self)
        ariaPathAct = QAction('Path', self)
        SettingMenu.addAction(LoginAct)
        SettingMenu.addAction(ariaPathAct)
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
        ariaPathAct.triggered.connect(self.setaria2Path)

        self.ftp = None
        self.userinfo = None
        self.timer = None
        self.aria2exepath = None
        self.aria2confpath = None
        self.aria2process = None
        if os.path.exists('./res/localFileInfo.json'):
            with open('./res/localFileInfo.json') as file:
                global localFileInfo
                localFileInfo = json.load(file)
        else:
            f = open('./res/localFileInfo.json', 'w')
            f.close()
        if os.path.exists('./res/fileInfo.json'):
            with open('./res/fileInfo.json') as file:
                filesInfo.update(json.load(file))
        else:
            f = open('./res/fileInfo.json', 'w')
            f.close()
        if os.path.exists('./res/aria2path.json'):
            with open('./res/aria2path.json', 'r') as file:
                d = json.load(file)
                self.aria2exepath = d['exePath']
                self.aria2confpath = d['confPath']
        if os.path.exists('./res/serverInfo.json'):
            with open('./res/serverInfo.json') as file:
                self.userinfo = json.load(file)
            self.ip = self.userinfo['ip']
            self.passwd = self.userinfo['passwd']
            self.username = self.userinfo['username']
            self.port = int(self.userinfo['port'])
            self.login()

    def setaria2Path(self):
        if not self.pathDlg:
            self.pathDlg = res.aria2pathDialog.ariapathDlg(self)
            self.pathDlg.okBtn.clicked.connect(self.getPath)
        if self.aria2exepath:
            self.pathDlg.exepathLineEdit.setText(self.aria2exepath)
        if self.aria2confpath:
            self.pathDlg.confpathLineEdit.setText(self.aria2confpath)
        self.pathDlg.show()

    def getPath(self):
        self.aria2exepath = self.pathDlg.exepathLineEdit.text()
        self.aria2confpath = self.pathDlg.confpathLineEdit.text()
        if self.aria2confpath != '' and self.aria2exepath != '':
            with open('./res/aria2path.json', 'w') as file:
                json.dump({
                    'exePath': self.aria2exepath,
                    'confPath': self.aria2confpath
                }, file)
        self.pathDlg.close()

    def showMenu(self, pos):
        for action in self.popMenu.actions():
            action.setEnabled(True)
        self.currentIndex = self.taskTable.indexAt(pos).row()
        if self.currentIndex < 0:
            for action in self.popMenu.actions():
                action.setEnabled(False)

        rows = []
        for itm in self.taskTable.selectionModel().selectedRows():
            rows.append(int(itm.row()))
        if len(rows)>1:
            self.popMenu.actions()[3].setEnabled(False)
            self.popMenu.actions()[4].setEnabled(False)
            self.popMenu.actions()[5].setEnabled(False)
            self.popMenu.actions()[6].setEnabled(False)
        elif len(rows)==1:
            if self.taskTable.item(int(rows[0]),3).text()!='complete':
                self.popMenu.actions()[3].setEnabled(False)
                self.popMenu.actions()[4].setEnabled(False)
                self.popMenu.actions()[5].setEnabled(False)
                self.popMenu.actions()[6].setEnabled(False)
            if self.taskTable.item(int(rows[0]),6).text()=='':
                self.popMenu.actions()[4].setEnabled(False)
                self.popMenu.actions()[5].setEnabled(False)
                self.popMenu.actions()[6].setEnabled(False)
            elif self.taskTable.item(int(rows[0]),6).text()=='paused':
                self.popMenu.actions()[3].setEnabled(False)
                self.popMenu.actions()[5].setEnabled(False)
            elif self.taskTable.item(int(rows[0]),6).text()=='complete':
                self.popMenu.actions()[3].setEnabled(False)
                self.popMenu.actions()[4].setEnabled(False)
                self.popMenu.actions()[5].setEnabled(False)
            else:
                self.popMenu.actions()[3].setEnabled(False)
                self.popMenu.actions()[4].setEnabled(False)               

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

    def login(self):
        if self.LoginWidget:
            self.ip = self.LoginWidget.IPLineEdit.text()
            self.passwd = self.LoginWidget.PasswdLineEdit.text()
            self.username = self.LoginWidget.UsernameLineEdit.text()
            self.port = int(self.LoginWidget.portLineEdit.text())
        try:
            self.ftp = openFtp(self.ip, self.port, self.username, self.passwd)
        except OSError:
            QMessageBox.critical(self.LoginWidget, 'Error', 'connection faild')
        else:
            if self.LoginWidget:
                self.LoginWidget.close()
            self.userinfo = {
                'ip': self.ip,
                'port': self.port,
                'username': self.username,
                'passwd': self.passwd
            }
            with open('./res/serverInfo.json', 'w+') as file:
                json.dump(self.userinfo, file)
            self.updateThread = UpdateFileStatus()
            self.updateLocalThread=UpdatelocalFileStatus()
            self.timer = QTimer(self)
            self.timer.timeout.connect(self.updateThread.start)
            self.timer.timeout.connect(self.updateLocalThread.start)
            self.updateThread.NewData.connect(self.updateFilelist)
            self.updateLocalThread.NewData.connect(self.updateLocalFileList)
            self.timer.start(3000)
            if self.aria2exepath and self.aria2confpath:
                if not os.path.exists(
                        self.aria2confpath.replace('aria2.conf',
                                                   'session.dat')):
                    f = open(
                        self.aria2confpath.replace('aria2.conf',
                                                   'session.dat'), 'w')
                    f.close()
                self.aria2process = subprocess.Popen(
                    self.aria2exepath + ' --conf-path ' + self.aria2confpath +
                    ' --save-session ' + self.aria2confpath.replace(
                        'aria2.conf', 'session.dat') + ' --input-file ' +
                    self.aria2confpath.replace('aria2.conf', 'session.dat'))
            self.getFileList()

    def updateFilelist(self, i, l, data):
        if len(data):
            status = data
            gid = l[i]
            if 'error' in status.keys():
                status=filesInfo[gid]
            filesInfo[gid] = status
            filename = status['result']['files'][0]['path'].split('/')[-1]
            linkaddress = status['result']['files'][0]['uris'][0]['uri']
            size = status['result']['files'][0]['length']
            offlinestatus = status['result']['status']
            if int(size) == 0:
                offlineprocess = str(format(0.00, '.2%'))
            else:
                offlineprocess = str(
                    format(
                        int(status['result']['completedLength']) / int(size),
                        '.2%'))
            offlinespeed = status['result']['downloadSpeed']
            self.taskTable.item(i, 0).setText(filename)
            self.taskTable.item(i, 1).setText(linkaddress)
            self.taskTable.item(i, 2).setText(size)
            self.taskTable.item(i, 3).setText(offlinestatus)
            self.taskTable.item(i, 4).setText(offlineprocess)
            self.taskTable.item(i, 5).setText(offlinespeed)

    def getFileList(self):
        self.taskTable.clearContents()
        for i in range(self.taskTable.rowCount()):
            self.taskTable.removeRow(i)
        for i, gid in enumerate(filesInfo.keys()):
            r = res.Sendcmd.SendCommand('tellStatus ' + gid,
                                        res.Sendcmd.server, res.Sendcmd.port)
            if r != 'error':
                status = json.loads(r)
                if 'error' in status.keys():
                    status=filesInfo[gid]
                filesInfo[gid] = status
                filename = status['result']['files'][0]['path'].split('/')[-1]
                linkaddress = status['result']['files'][0]['uris'][0]['uri']
                size = status['result']['files'][0]['length']
                offlinestatus = status['result']['status']
                if int(size) == 0:
                    offlineprocess = str(format(0.00, '.2%'))
                else:
                    offlineprocess = str(
                        format(
                            int(status['result']['completedLength']) /
                            int(size), '.2%'))
                offlinespeed = status['result']['downloadSpeed']
                retrivestatus = ''
                retrivespeed = ''
                savepath = ''
                filenameItem = QTableWidgetItem(filename)
                linkaddressItem = QTableWidgetItem(linkaddress)
                linkaddressItem.setToolTip(linkaddress)
                sizeItem = QTableWidgetItem(size)
                offlinestatusItem = QTableWidgetItem(offlinestatus)
                offlineprocessItem = QTableWidgetItem(offlineprocess)
                offlinespeedItem = QTableWidgetItem(offlinespeed)
                retrivestatusItem = QTableWidgetItem(retrivestatus)
                retrivespeedItem = QTableWidgetItem(retrivespeed)
                savepathItem = QTableWidgetItem(savepath)

                self.taskTable.insertRow(i)
                self.taskTable.setItem(i, 0, filenameItem)
                self.taskTable.setItem(i, 1, linkaddressItem)
                self.taskTable.setItem(i, 2, sizeItem)
                self.taskTable.setItem(i, 3, offlinestatusItem)
                self.taskTable.setItem(i, 4, offlineprocessItem)
                self.taskTable.setItem(i, 5, offlinespeedItem)
                self.taskTable.setItem(i, 6, retrivestatusItem)
                self.taskTable.setCellWidget(i, 7, QProgressBar(
                    self.taskTable))
                self.taskTable.cellWidget(i, 7).setMinimum(0)
                self.taskTable.cellWidget(i, 7).setMaximum(100)
                self.taskTable.setItem(i, 8, retrivespeedItem)
                self.taskTable.setItem(i, 9, savepathItem)
            else:
                self.taskTable.insertRow(i)
                self.taskTable.setItem(i, 0, QTableWidgetItem('Loading'))
                self.taskTable.setItem(i, 1, QTableWidgetItem('Loading'))
                self.taskTable.setItem(i, 2, QTableWidgetItem('Loading'))
                self.taskTable.setItem(i, 3, QTableWidgetItem('Loading'))
                self.taskTable.setItem(i, 4, QTableWidgetItem('Loading'))
                self.taskTable.setItem(i, 5, QTableWidgetItem('Loading'))

    def showAddUridlg(self):
        if not self.AddUridlg:
            self.AddUridlg = addUridlg(self)
            self.AddUridlg.OkBtn.clicked.connect(self.AddNewUri)
            self.AddUridlg.setModal(True)
        self.AddUridlg.show()

    def AddNewUri(self):
        duplicatelink = []
        for uri in self.AddUridlg.UriLineEdit.text().split():
            if uri in {
                    self.taskTable.item(i, 1).text()
                    for i in range(self.taskTable.rowCount())
            }:
                duplicatelink.append(uri)
        if len(duplicatelink):
            QMessageBox.information(
                self, 'Info',
                'duplicated Uri detected:' + ','.join(duplicatelink))
        newLinks = set(
            self.AddUridlg.UriLineEdit.text().split()) - set(duplicatelink)
        if len(newLinks):
            for link in newLinks:
                data = res.Sendcmd.SendCommand(
                    'addUri ' + link, res.Sendcmd.server, res.Sendcmd.port)
                if data != 'error':
                    j = json.loads(data)
                    gid = j['result']
                    filesInfo.update({gid: None})
                    localFileInfo.append([])
            self.getFileList()
        self.AddUridlg.close()
        self.AddUridlg.UriLineEdit.clear()

    def showAddTorrentdlg(self):
        pass

    def showAboutmedlg(self):
        pass

    def showAboutQtdlg(self):
        QMessageBox.aboutQt(self, 'About Qt')

    def showLocalDownloadDlg(self):
        if not self.retriveDlg:
            self.retriveDlg = retriveDlg(self)
            self.retriveDlg.setModal(True)
            self.retriveDlg.OkBtn.clicked.connect(self.getLocalPath)
        self.retriveDlg.show()

    def getLocalPath(self):
        LocalPath = self.retriveDlg.PathLineEdit.text()
        if not LocalPath or not os.path.exists(LocalPath):
            QMessageBox.critical(self, 'Invalid Path', 'Invalid Path')
        else:
            gid = res.Sendcmd.StartLocalDownload(
                self.taskTable.item(self.currentIndex, 0).text(),
                self.retriveDlg.ThreadSpinbox.value(), LocalPath)
            localFileInfo[self.currentIndex].append(gid)
            localFileInfo[self.currentIndex].append(LocalPath)
            if self.updateLocalThread.isFinished():
                self.updateLocalThread.start()
            self.retriveDlg.close()

    def updateLocalFileList(self,i,status):
        self.taskTable.item(i, 6).setText(status['status'])
        self.taskTable.item(i, 8).setText(status['downloadSpeed'])
        if status['dir']!='err':
            self.taskTable.item(i, 9).setText(status['dir'])
        else:
            self.taskTable.item(i,9).setText(localFileInfo[i][1])
        if int(status['totalLength']) != 0:
            self.taskTable.cellWidget(i, 7).setValue(
                (int(status['completedLength']
                        ) / int(status['totalLength'])) * 100)
        else:
            self.taskTable.cellWidget(i, 7).setValue(0)

    def Start_Server_Download_slot(self):
        rows = []
        for itm in self.taskTable.selectionModel().selectedRows():
            rows.append(int(itm.row()))
        for r in rows:
            gid = list(filesInfo.keys())[r]
            res.Sendcmd.SendCommand('unpause ' + gid, res.Sendcmd.server,
                                    res.Sendcmd.port)
        if self.updateThread.isFinished():
            self.updateThread.start()

    def Pause_Server_Download_slot(self):
        rows = []
        for itm in self.taskTable.selectionModel().selectedRows():
            rows.append(int(itm.row()))
        for r in rows:
            gid = list(filesInfo.keys())[r]
            res.Sendcmd.SendCommand('pause ' + gid, res.Sendcmd.server,
                                    res.Sendcmd.port)
        if self.updateThread.isFinished():
            self.updateThread.start()

    def Delete_Server_Download_slot(self):
        rows = []
        for itm in self.taskTable.selectionModel().selectedRows():
            rows.append(int(itm.row()))
        for r in sorted(rows, reverse=True):
            gid = list(filesInfo.keys())[r]
            res.Sendcmd.SendCommand('remove ' + gid, res.Sendcmd.server,
                                    res.Sendcmd.port)
            res.Sendcmd.SendCommand('removeDownloadResult ' + gid,
                                    res.Sendcmd.server, res.Sendcmd.port)
            res.Sendcmd.SendCommand(
                '_delLocalFile_ ' +
                filesInfo[gid]['result']['files'][0]['path'],
                res.Sendcmd.server, res.Sendcmd.port)
            del filesInfo[gid]
            if len(localFileInfo[r]):
                res.Sendcmd.DelLocalDownload(gid)
            localFileInfo.pop(r)
            self.taskTable.removeRow(r)
        if self.updateThread.isFinished():
            self.updateThread.start()

    def Pause_Retrieve_slot(self):
        res.Sendcmd.PauseLocalDownload(localFileInfo[self.currentIndex][0])

    def Delete_Retrieve_slot(self):
        res.Sendcmd.DelLocalDownload(localFileInfo[self.currentIndex][0])
        if os.path.exists(self.taskTable.item(self.currentIndex,9).text()):
            os.remove(self.taskTable.item(self.currentIndex,9).text())
        if os.path.exists(self.taskTable.item(self.currentIndex,9).text()+'.aria2'):
            os.remove(self.taskTable.item(self.currentIndex,9).text()+'.aria2')
    def Resume_Retrieve_slot(self):
        res.Sendcmd.ResumeLocalDownload(localFileInfo[self.currentIndex][0])

    def closeEvent(self, event):
        with open('./res/fileInfo.json', 'w') as file:
            json.dump(filesInfo, file)
        with open('./res/localFileInfo.json', 'w') as file:
            json.dump(localFileInfo, file)
        event.accept()
        if self.aria2process:
            self.aria2process.send_signal(signal.CTRL_C_EVENT)


class UpdateFileStatus(QThread):
    NewData = pyqtSignal(int, list, dict)

    def __init__(self):
        super().__init__()

    def run(self):
        keys = list(filesInfo.keys())
        for i, gid in enumerate(keys):
            r = res.Sendcmd.SendCommand('tellStatus ' + gid,
                                        res.Sendcmd.server, res.Sendcmd.port)
            if r != 'error':
                self.NewData.emit(i, keys, json.loads(r))
            else:
                self.NewData.emit(i, list(), dict())

class UpdatelocalFileStatus(QThread):
    NewData = pyqtSignal(int, dict)

    def __init__(self):
        super().__init__()

    def run(self):
        for i, gid in enumerate(localFileInfo):
            if len(gid):
                status = res.Sendcmd.CheckLocalDownloadStatus(gid[0])
                self.NewData.emit(i,status)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    mainwindow = Main()
    mainwindow.show()
    sys.exit(app.exec_())