#!/usr/bin/env python3
#-*- coding:utf-8 -*-

from pyftpdlib.servers import FTPServer
from pyftpdlib.authorizers import DummyAuthorizer
from pyftpdlib.handlers import TLS_FTPHandler
from pyftpdlib.filesystems import AbstractedFS

def runServer():
    authorizer=DummyAuthorizer()
    authorizer.add_user('PyOdUsEr','mG3Lfvl-!#','/data/downloads','elradfmwMT')
    handler=TLS_FTPHandler
    handler.certfile='/res/server.pem'
    handler.authorizer=authorizer
    handler.passive_ports=range(2222,3333)
    abfs=AbstractedFS
    abfs.fs2ftp('/data/downloads')
    handler.abstracted_fs=abfs
    server=FTPServer(('',2332),handler)
    server.serve_forever()

if __name__=='__main__':
    runServer()