#!/usr/bin/env python3
#-*- coding:utf-8 -*-

import subprocess, requests
import p_conf

status = subprocess.call(['mkdir', '/root/.aria2'], shell=False)
print('Downloading aria2')
url = 'https://github.com/q3aql/aria2-static-builds/releases/download/v1.32.0/aria2-1.32.0-linux-gnu-64bit-build1.tar.bz2'
r = requests.get(url)
with open('./res/aria2.tar.bz2', 'wb+') as file:
    file.write(r.content)
status = subprocess.call(['mkdir', './res/src'], shell=False)
status = subprocess.call(
    ['tar', 'jxvf', './res/aria2.tar.bz2', '-C', './res/src'], shell=False)
status = subprocess.call(
    ['make', '-C', './res/src/aria2-1.32.0-linux-gnu-64bit-build1', 'install'],
    shell=False)
p_conf.make_conf()