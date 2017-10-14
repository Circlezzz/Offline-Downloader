#!/usr/bin/env python3
#-*- coding:utf-8 -*-

import requests,json,socket

server='192.168.122.165'
port=26879

def SendCommand(cmds)
    sock=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    sock.connect((host,port))
    sock.send(cmds)
    data=sock.recv(1024)
    return data

SendCommand('')