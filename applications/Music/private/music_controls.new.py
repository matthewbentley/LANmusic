#!/usr/bin/python

import socket,os
import vlc
import os
from time import sleep

i=vlc.Instance()
p=i.media_player_new()

socketname="/tmp/music.sock"
queuenum=0
s = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
try:
    os.remove(socketname)
except OSError:
    pass
s.bind(socketname)
s.listen(1)
conn, addr = s.accept()
queuenum=0
while 1:
    sleep(5)
    data = conn.recv(1024)
    command = data.split(" ")
    if command[0] == "play":
        m=i.media_new("file://" + command[1])
        queuenum = command[2]
        p.set_media(m)
        p.play()
        break
    else:
        continue
        print p.get_length()-p.get_time()
conn.close()

while 1:
    if (p.get_length()-p.get_time() >= 5000) or (p.get_length() < 0):
        sleep(5)
    elif (p.get_length()-p.get_time() <= 1000) and (p.get_length() > 0):
        queuenum = int(queuenum)+1
        folder='uploads'
        try:
            filename = db.song(int(db.queue(queuenum).id)).file
        except:
            queuenum = 1
            filename = db.song(int(db.queue(queuenum).id)).fil
        path=os.path.join("/home/matthew/devel/music/", request.folder, folder, filename)
        m=i.media_new("file://"+path)
        p.set_media(m)
        p.play()
