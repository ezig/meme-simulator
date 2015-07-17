"""Reads in memetadata and creates a sentiment dictionary for words
Sentiment should heretoforth be known as 'dankness'
dankness is dependent on how many points the meme has
right now it can be any value, but might be scaled later
"""
import os
import re
import string
import sys


def load_dankness(path=DATA_PATH + "dankness.csv"):
    """Read the dankness file and return a dictionary containing the dankness
    score of each word
    """
    with open(path, encoding='utf8') as dankness_file:
        scores = [line.split(',') for line in dankness_file]
        return {word: float(score.strip()) for word, score in scores}