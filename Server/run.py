#!/usr/bin/env python3
#-*- coding:utf-8 -*-

import threading, requests, subprocess, json,socket

port=26879  #sever listen port
host=''     #listen client ip

commands_argv1='pauseAll unpauseAll tellActive tellWaiting tellStopped'.split()
commands_argv2_list='addUri addTorrent addMetalink'.split()
commands_argv2='remove pause unpause'.split()
commands_argv4='changePosition'.split()

token='Aa111111'

#CheckStatus
def CheckStatus(gid,token=''):
    jsonreq = json.dumps({
        'jsonrpc': '2.0',
        'id': 'qwer',
        'method': 'aria2.tellStatus',
        'params': ['token:' + token, gid]
    })
    r=requests.post('http://localhost:6800/jsonrpc',jsonreq)
    return r.text

#Start aria2 process
def StartProcess():
    child_process=subprocess.Popen(['/usr/bin/aria2c'])
    return child_process

#Deal with command sent by client
class GetCommand(threading.Thread):
    def __init__(self,lock,threadName,group):
        super().__init__(self,threadName,group=group)
        self.lock=lock

    def run():
        sock=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        sock.bind((host,port))
        sock.listen(5)
        while True:
            connection,address=sock.accept()
            data=connection.recv(1024)
            cmd=data.split()
            result=None
            if cmd[0] in commands_argv1:
                result=cmd_argv1(token,cmd[0])
                connection.send(result)
            elif cmd[0] in commands_argv2:
                result=cmd_argv2(token,cmd[1],cmd[0])
                connection.send(result)
            elif cmd[0] in commands_argv2_list:
                result=cmd_argv2_list(token,cmd[1:],cmd[0])
                connection.send(result)
            elif cmd[0] in commands_argv4:
                result=cmd_argv4(token,*cmd[1:],cmd[0])
                connection.send(result)
            elif cmd[0]=='tellStatus':
                CheckStatus(cmd[1],token=token)
            else:
                pass

# class SendInfo(threading.Thread):
#     def __init__(self,lock,threadName):
#         super().__init__(self,threadName)
#         self.lock=lock

#     def run():
#         pass

#command with 1 argv
def cmd_argv1(token,cmd):
    jsonreq = json.dumps({
        'jsonrpc': '2.0',
        'id': 'qwer',
        'method': 'aria2.'+cmd,
        'params': ['token:' + token]
    })
    r=requests.post('http://localhost:6800/jsonrpc',jsonreq)
    return r.text

#command with 2 argv
def cmd_argv2(token,pid,cmd):
    jsonreq = json.dumps({
        'jsonrpc': '2.0',
        'id': 'qwer',
        'method': 'aria2.'+cmd,
        'params': ['token:' + token,pid]
    })
    r=requests.post('http://localhost:6800/jsonrpc',jsonreq)
    return r.text

#command with 3 argv
def cmd_argv2_list(token,Uris,cmd):
    jsonreq = json.dumps({
        'jsonrpc': '2.0',
        'id': 'qwer',
        'method': 'aria2.'+cmd,
        'params': ['token:' + token,Uris]
    })
    r=requests.post('http://localhost:6800/jsonrpc',jsonreq)
    return r.text

#command with 4 argv
def cmd_argv4(token,gid,pos,how,cmd):
    jsonreq = json.dumps({
        'jsonrpc': '2.0',
        'id': 'qwer',
        'method': 'aria2.'+cmd,
        'params': ['token:' + token,gid,pos,how]
    })
    r=requests.post('http://localhost:6800/jsonrpc',jsonreq)
    return r.text

try:
    child_process=StartProcess()
    lock=threading.Lock()
    listen_thread=GetCommand(lock,'ListenThread',None)
    listen_thread.start()
except KeyboardInterrupt:
    raise(KeyboardInterrupt('interupted by user'))
finally:
    child_process.terminate()