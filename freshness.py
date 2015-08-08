"""Reads in memetadata and creates a sentiment dictionary for words
Where sentiment is ranked by "freshness", allowing us to creates
the freshest memes. Freshness is dependent on how many points the meme has
right now it can be any value, but might be scaled later
"""
import re
from models import *


def populate():
    """Avoiding regex for now
    """
    def data_source():
        words = {}
        for meme in Meme.select().where(Meme.score != 0):
            # join together top and bottom text
            if meme.top_text is None:
                meme.top_text = ''
            if meme.bottom_text is None:
                meme.bottom_text = ''
            text = meme.top_text + ' ' + meme.bottom_text

            # split the text on punctuation and spaces and iterate
            for word in filter(None, re.split("[., ]", text)):
                # if the word already exists, increase the count by 1
                # and update the freshness using a moving average
                if word in words:
                    freshness = words[word]['freshness']
                    count = words[word]['count']
                    words[word]['freshness'] = (meme.score + (freshness * count)) / (count + 1)
                    words[word]['count'] += 1
                # if the word doesn't exist, create an entry for it
                else:
                    words[word] = {}
                    words[word]['freshness'] = meme.score
                    words[word]['count'] = 1

        # convert the words dictionary into a format that can be inserted
        return [{'word':word, 'freshness':vals['count'], 'word_count':vals['freshness']} for word, vals in words.items()]

    initialize_db()
    data = data_source()
    with db.atomic():
        for i in range(0, len(data), 100):
            FreshWord.insert_many(data[i:i + 100]).execute()

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