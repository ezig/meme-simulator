> We don't read and write memes because it's cute. We read and write memes because we are members of the human race. And the human race is filled with passion. And medicine, law, business, engineering, these are noble pursuits and necessary to sustain life. But memes, dankness, macros, lulz, these are what we stay alive for. 

> -John Keating, Dead Poets Society

# meme-simulator

Uses Markov chains to generate text for image macros. Human-made image macro text is barely comprehensible English anyway, so you probably won't be able to tell the difference.

## How it Works

We use a [Markov Chain](https://en.wikipedia.org/wiki/Markov_chain) to generate text for each meme, having pulled many hundreds of thousands of memes from [Meme Generator's API](http://version1.api.memegenerator.net/) as reference.

We're currently in the process of optimizing how our Markov Chain selects the next word. Some paths we are looking at involve sentiment analysis, POS (parts of speech) detection, using databases such as WordNet, and other natural language processing libraries.

As a teaser, here is one of the best memes we have generated so far:

![generated meme](https://i.imgflip.com/odzyk.jpg)
