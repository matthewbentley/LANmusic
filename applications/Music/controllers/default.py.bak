# -*- coding: utf-8 -*-
# this file is released under public domain and you can use without limitations

#########################################################################
## This is a sample controller
## - index is the default action of any application
## - user is required for authentication and authorization
## - download is for downloading files uploaded in the db (does streaming)
## - call exposes all registered services (none by default)
#########################################################################


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
    print songsQ
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
    
    for i in songs:
        if i.song_id == request.args(0):
            redirect(URL('index',args='alreadythere'))
    
    db.queue.insert(title=db(db.song.id==request.args(0)).select()[0].title, song_id=request.args(0))
    redirect(URL('queue'))
    
def first():
    form = SQLFORM.factory(Field("visitor_name", label="What is your name?", requires=IS_NOT_EMPTY()))
    if form.process().accepted:
        session.visitor_name = form.vars.visitor_name
        redirect(URL('second'))
    return dict(form=form)
    
def second():
    name = session.visitor_name
    return dict(name=name)

def user():
    """
    exposes:
    http://..../[app]/default/user/login
    http://..../[app]/default/user/logout
    http://..../[app]/default/user/register
    http://..../[app]/default/user/profile
    http://..../[app]/default/user/retrieve_password
    http://..../[app]/default/user/change_password
    use @auth.requires_login()
        @auth.requires_membership('group name')
        @auth.requires_permission('read','table name',record_id)
    to decorate functions that need access control
    """
    return dict(form=auth())


@cache.action()
def download():
    """
    allows downloading of uploaded files
    http://..../[app]/default/download/[filename]
    """
    return response.download(request, db)


def call():
    """
    exposes services. for example:
    http://..../[app]/default/call/jsonrpc
    decorate with @services.jsonrpc the functions to expose
    supports xml, json, xmlrpc, jsonrpc, amfrpc, rss, csv
    """
    return service()


#@auth.requires_signature()
def data():
    """
    http://..../[app]/default/data/tables
    http://..../[app]/default/data/create/[table]
    http://..../[app]/default/data/read/[table]/[id]
    http://..../[app]/default/data/update/[table]/[id]
    http://..../[app]/default/data/delete/[table]/[id]
    http://..../[app]/default/data/select/[table]
    http://..../[app]/default/data/search/[table]
    but URLs must be signed, i.e. linked with
      A('table',_href=URL('data/tables',user_signature=True))
    or with the signed load operator
      LOAD('default','data.load',args='tables',ajax=True,user_signature=True)
    """
    return dict(form=crud())
