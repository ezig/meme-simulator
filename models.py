from peewee import *

db = SqliteDatabase('memes.db')

class MSModel(Model):
    class Meta:
        database = db

class MemeType(MSModel):
    id = PrimaryKeyField()

    meme_type_name = CharField (
        max_length=128, unique = True
    )

class Meme(MSModel):
    id = PrimaryKeyField()

    top_text = CharField(
        max_length=128
    )
    bottom_text = CharField(
        max_length=128
    )
    meme_type_id = ForeignKeyField(
        MemeType, relate_name='memes'
    )

class DankWord(MSModel):
    id = PrimaryKeyField()
    word = CharField(
        max_length = 128, unique = True
    )
    dankness = DoubleField(
        default = 0
    )
    count = IntegerField(
        default = 0
    )