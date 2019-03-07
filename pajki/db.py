from peewee import *

db = SqliteDatabase(None)

class URL(Model):
    content = TextField()
    url = CharField()

    class Meta:
        database = db
