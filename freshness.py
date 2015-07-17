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

def add_word(word, freshness):
    fresh_word = FreshWord.get_or_create(
        word=word
    )

    fresh_word.count += 1
    fresh_word.freshness = freshness
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