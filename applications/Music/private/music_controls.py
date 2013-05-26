#!/usr/bin/python

import socket,os
import vlc
import os

i=vlc.Instance()
p=i.media_player_new()

socketname="/tmp/music.sock"
queuenum=0
while 1:
    s = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
    try:
        os.remove(socketname)
    except OSError:
        pass
    s.bind(socketname)
    s.listen(1)
    conn, addr = s.accept()

    while 1:
        print p.get_length()-p.get_time()
        if (p.get_length()-p.get_time() <= 1000) and (p.get_length() > 0):
            queuenum = int(queuenum)+1
            print db.song(int(db.queue(queuenum).id)).file
            folder='uploads'
            print request.folder
            filename = db.song(int(db.queue(queuenum).id)).file
            path=os.path.join("/home/matthew/devel/music/", request.folder, folder, filename)
            m=i.media_new("file://"+path)
            p.set_media(m)
            p.play()
        data = conn.recv(1024)
        if not data: break
        command = data.split(" ")
        if command[0] == "play":
            m=i.media_new("file://" + command[1])
            queuenum = command[2]
            p.set_media(m)
            p.play()
        elif command[0] == "unpause":
            p.play()
        elif command[0] == "stop":
            p.stop()
        elif command[0] == "pause":
            p.pause()
        elif command[0] == "qnum":
            queuenum = command[1]
    conn.close()
