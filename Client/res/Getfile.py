#!/usr/bin/env python3 
#-*- coding:utf-8 -*-

import ftplib
import threading
import shutil
import os

ip='192.168.122.165'
port=2332
username='PyOdUsEr'
passwd='mG3Lfvl-!#'

class Done(Exception):
    pass

def openFtp(ip,port,username,passwd):
    ftp=ftplib.FTP()
    ftp.connect(ip,port)
    ftp.login(username,passwd)
    return ftp

class Ftpops():
    def __init__(self,threadNum):
        self.threadNum=threadNum
    
    def beginDownload(self,fileName,savePath):
        filesize=self.getFilesize(fileName)
        segmentsize=filesize//self.threadNum
        lastsegmentSize=0
        if filesize%self.threadNum!=0:
            lastsegmentSize=filesize-(segmentsize*(self.threadNum-1))
        
        Downloaders=list()
        for i in range(self.threadNum):
            if i==(self.threadNum-1):
                thissegSize=lastsegmentSize
            else:
                thissegSize=segmentsize
            Downloaders.append(Downloader(fileName,i,i*segmentsize,thissegSize))
        
        for d in Downloaders:
            d.thread.join()

        with open(savePath+'/'+fileName,'w+b') as f:
            for d in Downloaders:
                shutil.copyfileobj(open(d.segName,'rb'),f)
                os.remove(d.segName)

    def getFilesize(self,fileName):
        ftp=openFtp(ip,port,username,passwd)
        ftp.voidcmd('TYPE I')
        s=ftp.size(fileName)
        ftp.quit()
        return s

    def getFilelist(self):
        ftp=openFtp(ip,port,username,passwd)
        l=ftp.nlst()
        ftp.quit()
        return l

class Downloader():
    def __init__(self,fileName,segNum,segStart,segSize):
        self.fileName=fileName
        self.segNum=segNum
        self.segName=fileName+' '+str(self.segNum)
        self.segStart=segStart
        self.segSize=segSize
        self.ftp=openFtp(ip,port,username,passwd)
        self.file=open(self.segName,'a+b')
        self.thread=threading.Thread(target=self.receive_thread)
        self.thread.start()
    
    def receive_thread(self):
        try:
            self.ftp.retrbinary('RETR '+self.fileName,self.write_data,8192,self.segStart)
        except Done:
            pass
        finally:
            self.file.close()

    def write_data(self,data):
        self.file.write(data)
        if os.path.getsize(self.segName)>=self.segSize:
            self.file.truncate(self.segSize)
            raise(Done)


if __name__=='__main__':
    f=Ftpops(5)
    f.beginDownload('ASF-linux-x64.zip','/home/zhang')