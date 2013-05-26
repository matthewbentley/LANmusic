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
    songs = db().select(db.song.ALL, orderby=db.song.artist)
    return dict(message="Hello from my app!", counter=session.counter, songs=songs)

def up():
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
    redirect(URL('index'))
    return dict()

def down():
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
    redirect(URL('index'))
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
