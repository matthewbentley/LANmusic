#!/usr/bin/python

import socket,os
import vlc
import os
from time import sleep

i=vlc.Instance()
p=i.media_player_new()

socketname="/tmp/music.sock"
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
        pathO = command[3]
        p.set_media(m)
        p.play()
        break
    else:
        continue
conn.close()
sleep(5)
wait=False
skip=False
while 1:
    if wait:
        sleep(10)
        wait=False
    if (p.get_length()-p.get_time() >= 5000) or (p.get_length() < 0):
        sleep(5)
    elif (p.is_playing() == 0) or skip:
        if skip:
            skip=False
            p.stop()
        maxnum=db().select(db.queue.id, orderby=db.queue.id)[-1].id
        queuenum = int(queuenum)+1
        folder='uploads'
        try:
            filename = db.song(int(db.queue(queuenum).song_id)).file
        except:
            sleep(5)
            tryup=False
            while 1:
                try:
                    filename = db.song(int(db.queue(queuenum).song_id)).file
                    break
                except:
                    if (queuenum < maxnum) and tryup==True:
                        queuenum += 1
                    tryup=True
                    continue
        path=os.path.join(pathO, folder, filename)
        m=i.media_new("file://"+path)
        p.set_media(m)
        p.play()
        wait=True
    newcommand=[]
    socketname="/tmp/music.sock"
    s = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
    try:
        os.remove(socketname)
    except OSError:
        pass
    s.bind(socketname)
    s.listen(1)
    try:
        s.settimeout(5)
        conn, addr = s.accept()
        while 1:
            data = conn.recv(1024)
            if not data: break
            newcommand=data.split(" ")
            if newcommand[0] == "next":
                if queuenum == newcommand[1]:
                    skip=True
    except:
        pass
