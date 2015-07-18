"""Reads in memetadata and creates a sentiment dictionary for words
Where sentiment is ranked by "freshness", allowing us to creates
the freshest memes. Freshness is dependent on how many points the meme has
right now it can be any value, but might be scaled later
"""
import os
import re
import string
import sys
from models import *

from peewee import *


def populate():
    """Avoiding regex for now
    """
    for meme in Meme.select().where(Meme.score != 0):
        if meme.top_text is None:
            meme.top_text = ''
        if meme.bottom_text is None:
            meme.bottom_text = ''
        text = meme.top_text + ' ' + meme.bottom_text
        text = text.replace(',', ' ').lower()
        text = text.replace('.', ' ')
        words = text.split()
        for word in words:
            fresh_word, created = FreshWord.get_or_create(
                word = word,
                defaults={'freshness': meme.score, 'word_count': 1}
            )
            if not created:
                fresh_word.freshness = (meme.score + (fresh_word.freshness * fresh_word.word_count)) / (fresh_word.word_count + 1)
                fresh_word.word_count += 1
                fresh_word.save()


def get_word_freshness(word_list):
    """Makes a DB query and returns a list of the words ordered by
    their freshness
    """
    return (FreshWord
                .select()
                .where(FreshWord.word << word_list)
                .order_by(FreshWord.freshness.desc()))

def get_freshest_word(word_list):
    """Makes a DB query and returns the freshest word of the list
    """
    return get_word_freshness(word_list)[0]

# def load_dankness(path=DATA_PATH + "dankness.csv"):
#     """Read the dankness file and return a dictionary containing the dankness
#     score of each word
#     """
#     with open(path, encoding='utf8') as dankness_file:
#         scores = [line.split(',') for line in dankness_file]
#         return {word: float(score.strip()) for word, score in scores}