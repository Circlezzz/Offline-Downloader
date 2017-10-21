#!/usr/bin/env python3
#-*- coding:utf-8 -*-

import threading, requests, subprocess, json,socket,os,signal,multiprocessing,time
from file_transfer import runFTPServer

port=26879  #sever listen port
host=''     #listen client ip

#supported commands
commands_argv1='pauseAll unpauseAll tellActive tellWaiting tellStopped'.split()
commands_argv2_list='addUri addTorrent addMetalink'.split()
commands_argv2='remove pause unpause removeDownloadResult getFiles tellStatus'.split()
commands_argv4='changePosition'.split()

#secure token
token='Passw0rd'

#CheckStatus
# def CheckStatus(gid,token=''):
#     jsonreq = json.dumps({
#         'jsonrpc': '2.0',
#         'id': 'qwer',
#         'method': 'aria2.tellStatus',
#         'params': ['token:' + token, gid]
#     })
#     r=requests.post('http://localhost:6800/jsonrpc',jsonreq)
#     return r.text

#Start aria2 process
def StartariaProcess():
    # rpip,wpip=os.pipe()
    pid=os.fork()   #fork twice to avoid defunct process
    if pid==0:#subprocess
        pid2=os.fork()
        if pid2==0:#grandson process
            grandson_process=subprocess.Popen(['/usr/bin/aria2c'])
            try:
                grandson_process.wait()
            except KeyboardInterrupt:
                print('Interrupted by user---------aria2')
                os._exit(0)
        else:
            #os.write(wpip,str(pid2).encode('utf8'))
            os._exit(0)
    else:
        # fobj=os.fdopen(rpip,'r')
        # recv=os.read(rpip,32)
        os.wait()
        # return int(recv)


# #Start FTP process
# def StartFTPProcess():
#     # rpip,wpip=os.pipe()
#     pid=os.fork()   #fork twice to avoid defunct process
#     if pid==0:#subprocess
#         pid2=os.fork()
#         if pid2==0:#grandson process
#             try:
#                 runFTPServer()
#                 print('5')
#             except KeyboardInterrupt:
#                 print('Interrupted by user----------FTP')
#                 os._exit(0)
#         else:
#             #os.write(wpip,str(pid2).encode('utf8'))
#             print('1')
#             os._exit(0)
#     else:
#         # fobj=os.fdopen(rpip,'r')
#         # recv=os.read(rpip,32)
#         os.wait()
#         print('2')
#         # return int(recv)

#Deal with command sent by client
class GetCommand(multiprocessing.Process):
    def __init__(self):
        super().__init__()
    
    # def bindsocket(self):
    #     try:
    #         self.sock.bind((host,port))
    #     except OSError:
    #         print('Trying to bind socket...')
    #         time.sleep(5)
    #         self.bindsocket()
    #     except KeyboardInterrupt:
    #         pass

    def run(self):
        print(4)
        self.sock=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.sock.bind((host,port))
        print('Socket binded')
        self.sock.listen(20)
        try:
            while True:
                connection,address=self.sock.accept()
                data=connection.recv(1024)
                data=data.decode('utf8')
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
                    connection.send(result))                
                elif cmd[0] in commands_argv4:
                    result=cmd_argv4(token,*cmd[1:],cmd[0])
                    connection.send(result)
                elif cmd[0] =='_delLocalFile_':
                    flag=True
                    print(cmd)
                    if len(cmd)==1:
                        flag=False
                    if flag and os.path.exists(cmd[1]):
                        os.remove(cmd[1])
                    if flag and os.path.exists(cmd[1]+'.aria2'):
                        os.remove(cmd[1]+'.aria2')
                    connection.send('Ok'.encode('utf8'))
                else:
                    connection.send('Wrong command'.encode('utf8'))
        except KeyboardInterrupt:
                print('Interrupted by user-------socket')
        finally:
                print('3')
                time.sleep(1)
                self.sock.shutdown(2)
                self.sock.close()
                os._exit(0)
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
    return r.content

#command with 2 argv
def cmd_argv2(token,pid,cmd):
    jsonreq = json.dumps({
        'jsonrpc': '2.0',
        'id': 'qwer',
        'method': 'aria2.'+cmd,
        'params': ['token:' + token,pid]
    })
    r=requests.post('http://localhost:6800/jsonrpc',jsonreq)
    return r.content

#command with 2 argv(list)
def cmd_argv2_list(token,Uris,cmd):
    jsonreq = json.dumps({
        'jsonrpc': '2.0',
        'id': 'qwer',
        'method': 'aria2.'+cmd,
        'params': ['token:' + token,Uris]
    })
    r=requests.post('http://localhost:6800/jsonrpc',jsonreq)
    return r.content

#command with 4 argv
def cmd_argv4(token,gid,pos,how,cmd):
    jsonreq = json.dumps({
        'jsonrpc': '2.0',
        'id': 'qwer',
        'method': 'aria2.'+cmd,
        'params': ['token:' + token,gid,pos,how]
    })
    r=requests.post('http://127.0.0.1:6800/jsonrpc',jsonreq)
    return r.content

StartariaProcess()
# StartFTPProcess()
# print('Process Started')
ftp_process=multiprocessing.Process(target=runFTPServer)
ftp_process.start()
listen_process=GetCommand()
listen_process.start()
try:
    listen_process.join()
except KeyboardInterrupt:
    print('Interrupted by user')