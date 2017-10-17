#!/usr/bin/env python3 
#-*- coding:utf-8 -*-

import ftplib

def connectServer():
    ftps=ftplib.FTP_TLS()
    ftps.connect('192.168.122.165',2332)
    ftps.login('PyOdUsEr','mG3Lfvl-!#')
    ftps.prot_p()
    print(ftps.nlst())

if __name__=='__main__':
    connectServer()