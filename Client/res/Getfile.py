#!/usr/bin/env python3 
#-*- coding:utf-8 -*-

import ftplib

def connectServer():
    ftps=ftplib.FTP()
    ftps.connect('192.168.122.165',2332)
    ftps.login('PyOdUsEr','mG3Lfvl-!#')
    print(ftps.nlst())

if __name__=='__main__':
    connectServer()