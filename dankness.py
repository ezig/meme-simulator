"""Reads in memetadata and creates a sentiment dictionary for words
Sentiment should heretoforth be known as 'dankness'
dankness is dependent on how many points the meme has
right now it can be any value, but might be scaled later
"""
import os
import re
import string
import sys
from peewee import *


def select_dank_words(word_list):
    """Makes a DB query and returns a list of the words ordered by
    their dankness
    """
    return User.select(User.word).where(User.word in word_list).order_by(User.dankness)

def select_dankest_word(word_list):
    """Makes a DB query and returns the dankest word of the list
    """
    dank_words = select_dank_words(word_list)
    return dank_words[0]

def load_dankness(path=DATA_PATH + "dankness.csv"):
    """Read the dankness file and return a dictionary containing the dankness
    score of each word
    """
    with open(path, encoding='utf8') as dankness_file:
        scores = [line.split(',') for line in dankness_file]
        return {word: float(score.strip()) for word, score in scores}