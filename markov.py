import random as rand
import sqlite3
import os

from models import *

class Markov(object):
    def __init__(self, meme_type, is_top_text):
        self.meme_type = meme_type
        self.is_top_text = is_top_text

    def gen_cache(self):
        # create a hash that maps each pair of consecutive words to all of the
        # words that follow the pair in the input text
        def data_source():
            entries = []
            for meme in self.meme_type.memes:
                text = ""

                if self.is_top_text:
                    text = meme.top_text
                else:
                    text = meme.bottom_text

                if not text:
                    continue

                text = text.upper().split()

                if len(text) < 3:
                    continue

                entries.append(self.cache_entry("", "", text[0]))
                entries.append(self.cache_entry("", text[0], text[1]))

                for i in range(0, len(text) - 2):
                    entries.append(self.cache_entry(text[i], text[i + 1], text[i + 2]))

                entries.append(self.cache_entry(text[-2], text[-1], ""))
                entries.append(self.cache_entry(text[-1], "", ""))

            return entries

        with db.atomic():
            data = data_source()
            for i in range (0, len(data), 100):
                MarkovEntry.insert_many(data[i:i + 100]).execute()

    def gen_text(self, size):
        # returns a string generated from the cache of `size` length
        word_list = []

        word1 = rand.choice(self.lookup("", ""))
        word2 = rand.choice(self.lookup("", word1))

        for _ in range(size):
            word_list.append(word1)
            state = (word1, word2)

            # get a word that follows the current state
            word1, word2 = word2, rand.choice(self.lookup(word1, word2))

            if word1 == "":
                break

        # concat together all of the words in the list
        return " ".join(word_list)

    def cache_entry(self, word1, word2, word3):
        return {'word1': word1,
         'word2':word2,
          'word3':word3,
          'is_top_text':self.is_top_text,
          'meme_type_id':self.meme_type}

    def lookup(self, word1, word2):
        word_list = []

        conn = sqlite3.connect(dbname)
        c = conn.cursor()
        for row in c.execute("""SELECT * FROM markoventry
                     WHERE word1 = ?
                     AND word2 = ?
                     AND is_top_text = ?
                     AND meme_type_id_id = ?""",
                     (word1, word2, int(self.is_top_text), self.meme_type.id)):
            word_list.append(row[3])
        conn.close()

        return word_list

class Memekov(object):
    def __init__(self, meme_type):
        self.tt = Markov(meme_type, True)
        self.bt = Markov(meme_type, False)

    def gen_cache(self):
        self.tt.gen_cache()
        self.bt.gen_cache()

    def gen_meme(self, size):
        return (self.tt.gen_text(size), self.bt.gen_text(size))

initialize_db()

mk = Memekov(MemeType.get(MemeType.id==1))

for i in range(0, 1):
    print(mk.gen_meme(100))
