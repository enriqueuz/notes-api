""" Note models """
import peewee
import datetime

from hashlib import sha1
from random import random
from playhouse.sqlite_ext import SqliteExtDatabase

#db = peewee.SqliteDatabase('notes.db')
db = SqliteExtDatabase('notes.db')

class BaseModel(peewee.Model):
    """ Base model """
    class Meta:
        """ Meta class """
        database = db

class Note(BaseModel):
    """ Model to store Notes data. """
    title = peewee.CharField(max_length=60)
    content = peewee.TextField()
    created = peewee.DateTimeField(default=datetime.datetime.now)


class User(BaseModel):
    """ Model to store Users data. """
    username = peewee.CharField(unique=True, max_length=60)
    password = peewee.CharField(max_length=60)
    join_date = peewee.DateTimeField(default=datetime.datetime.now)

# Data base functions for passwords hashing     

def get_hexdigest(salt, raw_password):
    data = salt + raw_password
    return sha1(data.encode('utf8')).hexdigest()

@db.func()
def make_password(raw_password):
    salt = get_hexdigest(str(random()), str(random()))[:5]
    hsh = get_hexdigest(salt, raw_password)
    return '%s$%s' % (salt, hsh)

@db.func()
def check_password(raw_password, enc_password):
    salt, hsh = enc_password.split('$', 1)
    return hsh == get_hexdigest(salt, raw_password)

def initialize():
    """ Create tables """
    db.connect()
    db.create_tables([Note, User], safe = False)
    db.close()