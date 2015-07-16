require 'rubygems'
require 'json'
require 'net/http'
require_relative 'markov.rb'

 url = "http://version1.api.memegenerator.net/Instances_Select_ByPopular?languageCode=en&pageIndex=0&pageSize=24"
 resp = Net::HTTP.get_response(URI.parse(url))
 data = resp.body

 result = JSON.parse(data)

 top_text = ""
 bottom_text = ""

 for meme in result["result"]
   if meme["text0"]
     top_text += meme["text0"] + " "
   end

   if meme["text1"]
     bottom_text += meme["text1"] + " "
   end
 end

top = Markov.new("top", top_text)
bottom = Markov.new("bottom", bottom_text)
puts top.gen_text(10)
puts bottom.gen_text(10)
