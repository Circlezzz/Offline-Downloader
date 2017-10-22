#!/usr/bin/env python3
#-*- coding:utf-8 -*-

import requests, json, socket

server = '192.168.204.128'
port = 26879


def SendCommand(cmds, server, port):
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
        data = sock.recv(1024)
    except socket.timeout:
        return 'error'
    else:
        return data.decode('utf8')
    finally:
        sock.close()


if __name__ == '__main__':
    a = SendCommand('addUri https://github.com/JustArchi/ArchiSteamFarm/releases/download/3.0.3.6/ASF-linux-x64.zip',server,port)
    import json
    j=json.loads(a)
    b=j['result']
    import time

    def test():
        print(SendCommand('getFiles ' + b, server, port))
        time.sleep(2)
        test()

    test()
