class Markov
  def initialize(name, input_text)
    @name = name
    @input_text = input_text
    @words = input_text.split
    @cache = {}

    gen_cache
  end

  def gen_cache
    # create a hash that maps each pair of consecutive words to all of the
    # words that follow the pair in the input text
    for i in 0...(@words.length - 2) do
      state = [@words[i], @words[i + 1]]

      if @cache.has_key?(state)
        @cache[state].push(@words[i + 2])
      else
        @cache[state] = [@words[i + 2]]
      end
    end
  end

  def gen_text(size)
    # returns a string generated from the cache of `size` length
    word_list = []

    rand_idx = Random.rand(@words.length - 2)
    word1 = @words[rand_idx]
    word2 = @words[rand_idx + 1]

    size.times do
      word_list.push(word1)
      state = [word1, word2]

      if @cache.has_key?(state)
        # get a word that follows the current state
        word1, word2 = word2, @cache[state].sample
      else
        # rare case where we get to a the very last three words in the text
        # and there is no next word
        rand_idx = Random.rand(@words.length - 2)
        word1 = @words[rand_idx]
        word2 = @words[rand_idx + 1]
      end
    end

    # concat together all of the words in the list
    output_text =  word_list.inject("") {|text, word| text + " " + word}
    # get rid of the extra space at the very beginning
    output_text[0] = ''
    return output_text
  end
end
