import random as rand
import pickle
import os

from models import *

class Markov(object):
    def __init__(self, text_list, cache_file):
        self.text_list = text_list
        self.cache = {}

        if os.path.exists(cache_file):
            try:
                with open(cache_file, 'rb') as f:
                    self.cache = pickle.load(f)
            except:
                raise
        else:
            self.gen_cache()

            with open(cache_file, 'wb') as f:
                pickle.dump(self.cache, f)


    def gen_cache(self):
        # create a hash that maps each pair of consecutive words to all of the
        # words that follow the pair in the input text
        for text in self.text_list:
            if not text:
                continue

            text = text.upper().split()

            if len(text) < 3:
                continue

            self.update_cache(("", ""), text[0])
            self.update_cache(("", text[0]), text[1])

            for i in range(0, len(text) - 2):
                self.update_cache((text[i], text[i + 1]), text[i + 2])

            self.update_cache((text[-2], text[-1]), "")
            self.update_cache((text[-1], ""), "")

    def update_cache(self, state, word):
        if state in self.cache:
            self.cache[state].append(word)
        else:
            self.cache[state] = [word]

    def gen_text(self, size):
        # returns a string generated from the cache of `size` length
        word_list = []

        word1 = rand.choice(self.cache[("","")])
        word2 = rand.choice(self.cache[("", word1)])

        for _ in range(size):
            word_list.append(word1)
            state = (word1, word2)

            # get a word that follows the current state
            word1, word2 = word2, rand.choice(self.cache[state])

            if word1 == "":
                break

        # concat together all of the words in the list
        output_text = ""
        for word in word_list:
            output_text += " " + word
        # get rid of the extra space at the very beginning
        return output_text[1:]

top_text = []
bottom_text = []

for meme in MemeType.get(meme_type_name="Futurama-Fry").memes:
    top_text.append(meme.top_text)
    bottom_text.append(meme.bottom_text)

top_gen = Markov(top_text, 'data/top_markov_cache.p')
bottom_gen = Markov(bottom_text, 'data/bottom_markov_cache.p')

for i in range(10):
    print(top_gen.gen_text(100))
    print(bottom_gen.gen_text(100))
