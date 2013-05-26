# -*- coding: utf-8 -*-
# this file is released under public domain and you can use without limitations

#########################################################################
## This is a sample controller
## - index is the default action of any application
## - user is required for authentication and authorization
## - download is for downloading files uploaded in the db (does streaming)
## - call exposes all registered services (none by default)
#########################################################################
import os
import vlc
import socket

def index():
    """
    example action using the internationalization operator T and flash
    rendered by views/default/index.html or views/generic.html

    if you need a simple wiki simple replace the two lines below with:
    return auth.wiki()
    """
    session.counter=(session.counter or 0) + 1
    if request.args(0) == "alreadythere":
        response.flash = "Sorry, that song is already in the queue"
    elif request.args(0) == "tolowscore":
        response.flash = "Sorry, that song has to many down votes"
    songs = db().select(db.song.ALL, orderby=db.song.artist)
    return dict(message="Hello from my app!", counter=session.counter, songs=songs)

def play(song_id,queuenum):
    song = get_path(song_id)
    folder='uploads'
    send_to_sock('/tmp/music.sock', "play " + song + " " + str(queuenum) + " " + request.folder)
    
def stop():
    send_to_sock('/tmp/music.sock', 'stop')
    
def changeQueueNum(x):
    send_to_sock('/tmp/music.sock', 'qnum ' + x)

def send_to_sock(connto,data):
    s = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
    s.connect(connto)
    s.send(data)
    s.close()

def get_path(song_id,folder='uploads'):
    filename = db.song(song_id).file
    path=os.path.join(request.folder, folder, filename)
    return path

def upq():
    up('queue')
    
def downq():
    down('queue')

def upi():
    up('index')
    
def downi():
    down('index')

def up(returnto):
    song_id=request.args(0)
    up = db.song(song_id).up_votes
    down = db.song(song_id).down_votes
    if session.song_id == "up":
        pass
    elif session.song_id == "down":
        down-=1
        up+=1
        db(db.song.id == song_id).update(up_votes=up)
        db(db.song.id == song_id).update(down_votes=down)
    else:
        up+=1
        db(db.song.id == song_id).update(up_votes=up)
    session.song_id = "up"
    redirect(URL(returnto))
    return dict()

def removeLowVotes(song_id):
    songsQ = db(db.queue.song_id == song_id).select(db.queue.ALL, orderby=db.queue.id)
    songsO = db(db.song.id == song_id).select(db.song.ALL, orderby=db.song.id)
    if int(songsO[0].down_votes)/3 >= int(songsO[0].up_votes):
        try:
            if songsQ[0]:
                db(db.queue.song_id == song_id).delete()
        except:
            pass

def down(returnto):
    song_id=request.args(0)
    up = db.song(song_id).up_votes
    down = db.song(song_id).down_votes
    if session.song_id == "down":
        pass
    elif session.song_id == "up":
        down+=1
        up-=1
        db(db.song.id == song_id).update(up_votes=up)
        db(db.song.id == song_id).update(down_votes=down)
    else:
        down+=1
        db(db.song.id == song_id).update(up_votes=up)
    session.song_id = "down"
    removeLowVotes(song_id)
    redirect(URL(returnto))
    return dict()

def upload():
    form = SQLFORM(db.song, deletable=True, upload=URL('download'))
    if form.process().accepted:
        response.flash = "Form accepted"
        song_id = form.vars.id
        session.song_id = "up"
        redirect(URL('index'))
    elif form.errors:
        response.flash = "Form has errors"
    return dict(form=form)
    
def queue():
    songs = db().select(db.queue.ALL, orderby=db.queue.id)
    songsO = db().select(db.song.ALL, orderby=db.song.id)
    return dict(songs=songs, songsO=songsO)
    
def addtoqueue():
    if not request.args(0):
        redirect(URL('index'))
    songs = db().select(db.queue.ALL, orderby=db.queue.id)
    songsO = db(db.song.id == request.args(0)).select(db.song.ALL, orderby=db.song.id)
    
    if int(songsO[0].down_votes)/2 >= int(songsO[0].up_votes):
        redirect(URL('index',args='tolowscore'))
    count=0
    start=False
    for i in songs:
        count+=1
        if i.song_id == request.args(0):
            redirect(URL('index',args='alreadythere'))
    if count==0:
        start=True
    
    db.queue.insert(title=db(db.song.id==request.args(0)).select()[0].title, song_id=request.args(0))
    if start:
        play(db(db.queue.id == 1).select(db.queue.song_id)[0].song_id,1)
    redirect(URL('queue'))
