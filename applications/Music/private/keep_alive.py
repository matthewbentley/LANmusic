#!/usr/bin/bash
import os,socket
from time import sleep
while 1:
    s = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
    s.connect('/tmp/music.sock')
    s.send("")
    s.close()
    sleep(5)
