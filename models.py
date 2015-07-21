from peewee import *

db = SqliteDatabase('data/memes.db')

def initialize_db():
    db.connect()
    db.create_tables([MemeType, Meme, FreshWord, Markov], safe=True)

class MSModel(Model):
    class Meta:
        database = db

class MemeType(MSModel):
    id = PrimaryKeyField()

    meme_type_name = CharField (
        max_length=128, unique = True, index = True
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
        MemeType, related_name='memes'
    )
    score = IntegerField(
        default=0
    )
    class Meta:
        indexes = (
            (('top_text', 'bottom_text'), True),
        )

class Markov(MSModel):
    id = PrimaryKeyField()

    word1 = CharField (
        max_length=24
    )
    word2 = CharField (
        max_length=24
    )
    word3 = CharField (
        max_length=24
    )
    is_top_text = BooleanField()
    meme_type_id = ForeignKeyField(
        MemeType, related_name='markovs'
    )
    class Meta:
        indexes = (
            (('word1', 'word2'), False)
        )

class FreshWord(MSModel):
    id = PrimaryKeyField()
    word = CharField(
        max_length=128, unique=True, index =True
    )
    freshness = DoubleField(
        default=0
    )
    word_count = IntegerField(
        default=0
    )
