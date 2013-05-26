# -*- coding: utf-8 -*-

db = DAL("sqlite://storage.sqlite")

db.define_table('song', Field('file','upload'), Field('title'), Field('artist'), Field('album'), Field('track_number'), Field('up_votes','integer',default=1), Field('down_votes','integer',default=0))

db.define_table('queue', Field('file'))

db.song.file.requires = db.song.title.requires = db.song.artist.requires = IS_NOT_EMPTY()
db.queue.file.requires = IS_NOT_EMPTY()
db.queue.file.requires = IS_IN_DB(db, db.song.file)

db.song.up_votes.writable = db.song.up_votes.readable = False
db.song.down_votes.writable = db.song.down_votes.readable = False
