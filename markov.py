import random

class Markov(object):
    def __init__(self, name, input_text):
        self.name = name
        self.input_text = input_text
        self.words = input_text.split(" ")
        self.cache = {}

        self.gen_cache()

    def gen_cache(self):
        # create a hash that maps each pair of consecutive words to all of the
        # words that follow the pair in the input text
        for i in range(0, len(self.words) - 2):
            state = (self.words[i], self.words[i + 1])

            if state in self.cache:
                self.cache[state].append(self.words[i + 2])
            else:
                self.cache[state] = [self.words[i + 2]]

    def gen_text(self, size):
        # returns a string generated from the cache of `size` length
        word_list = []

        rand_idx = random.randint(0, len(self.words) - 2)
        word1 = self.words[rand_idx]
        word2 = self.words[rand_idx + 1]

        for _ in range(size):
            word_list.append(word1)
            state = (word1, word2)

            if state in self.cache:
                # get a word that follows the current state
                word1, word2 = word2, random.choice(self.cache[state])
            else:
                # rare case where we get to a the very last three words in the text
                # and there is no next word
                rand_idx = random.randint(0, len(self.words) - 2)
                word1 = self.words[rand_idx]
                word2 = self.words[rand_idx + 1]

        # concat together all of the words in the list
        output_text = reduce(lambda text, word : text + " " + word, word_list, "")
        # get rid of the extra space at the very beginning
        return output_text[1:]
