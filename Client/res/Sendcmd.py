#!/usr/bin/env python3
#-*- coding:utf-8 -*-

import requests, json, socket
import xmlrpc.client

server = '192.168.204.128'
port = 26879


def SendCommand(cmds, server, port):
    def send():
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(2)
        try:
            sock.connect((server, port))
        except OSError:
            print('Failed to connect')
            sock.close()
            return 'error'

        sock.send(cmds.encode('utf8'))
        try:
            data = sock.recv(4096)
        except socket.timeout:
            return 'error'
        else:
            return data.decode('utf8')
        finally:
            sock.close()

    result='error'
    while result=='error':
        result=send()
    return result

def StartLocalDownload(filename,thread,path):
    s=xmlrpc.client.ServerProxy('http://localhost:6800/rpc')
    r=s.aria2.addUri(['ftp://192.168.204.128/'+filename],{'dir':path,'max-connection-per-server':thread,'split':thread})
    return r


def CheckLocalDownloadStatus(gid):
    s=xmlrpc.client.ServerProxy('http://localhost:6800/rpc')
    try:
        r=s.aria2.tellStatus(gid)
    except xmlrpc.client.Fault:
        return {'status':'complete','downloadSpeed':'0','dir':'err','totalLength':'1','completedLength':'1'}
    else:
        return r

def DelLocalDownload(gid):
    s=xmlrpc.client.ServerProxy('http://localhost:6800/rpc')
    try:
        r=s.aria2.remove(gid)
    except xmlrpc.client.Fault:
        return {}
    try:
        r=s.aria2.removeDownloadResult(gid)
    except xmlrpc.client.Fault:
        return {}

def PauseLocalDownload(gid):
    s=xmlrpc.client.ServerProxy('http://localhost:6800/rpc')
    r=s.aria2.pause(gid)

def ResumeLocalDownload(gid):
    s=xmlrpc.client.ServerProxy('http://localhost:6800/rpc')
    r=s.aria2.unpause(gid)


if __name__ == '__main__':
    a = SendCommand('addUri https://github.com/JustArchi/ArchiSteamFarm/releases/download/3.0.3.6/ASF-linux-x64.zip https://github.com/JustArchi/ArchiSteamFarm/releases/download/3.0.4.0/ASF-linux-arm.zip https://github.com/JustArchi/ArchiSteamFarm/releases/download/3.0.4.0/ASF-win-x64.zip',server,port)
    import json
    j=json.loads(a)
    b=j['result']
    import time

    def test():
        print(SendCommand('getFiles ' + b, server, port))
        time.sleep(2)
        test()

    test()
