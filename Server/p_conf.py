#!/usr/bin/env python3
#-*- coding:utf-8 -*-

import requests
import subprocess

download_directory='/data/downloads'
user_home='/root'

def make_conf():
    print('making configure file')
    l = list()
    r = requests.get(
        'https://raw.githubusercontent.com/ngosang/trackerslist/master/trackers_all_udp.txt'
    )
    with open('./res/bt-list', 'w') as file:
        file.write(r.text)

    with open('./res/bt-list', 'r') as file:
        while True:
            data = file.readline()
            if data:
                if data != '\n':
                    l.append(data.replace('\n', ''))
            else:
                break

    with open('./res/aria2_temp.conf', 'r') as file:
        content = file.read()
        content.replace('dir=/data/downloads','dir='+download_directory)
        with open(user_home+'/.aria2/aria2.conf', 'w') as file2:
            file2.write(content + 'bt-tracker=' + ','.join(l))
    
    status=subprocess.call(['mkdir','-p',download_directory],shell=False)
