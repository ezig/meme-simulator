"""Requests meme metadata (memetadata) from memegenerator's API
"""

from models import *

import requests
import json
import sys
import os

base_data_uri = "http://version1.api.memegenerator.net/Instances_Select_ByNew"
base_gen_uri = "http://version1.api.memegenerator.net/Generators_Search"

meme_names = ['Futurama', 'Success', 'Interesting', 'Willywonka', 'Philosoraptor', 'Simply', 'Brian', 'Greg', 'Scumbag']

"""Keep in case my method failed
meme_name_dictionary = {'Y-U-No': 2287719, 'Futurama-Fry': 1461840, 'Success-Kid': 1190989,
                        'The-Most-Interesting-Man-In-The-World': 1239075, 'Willywonka': 985064,
                        'Philosoraptor': 733671, 'One-Does-Not-Simply-A': 1146447,
                        'Bad-Luck-Brian-Meme': 653934, 'Good-Guy-Greg': 338941}
"""


initialize_db()

def get_meme_dictionary(meme_names):
	"""Gets the highest ranking meme generator for each meme in meme_names, returns a dictionary that maps
	the urlName for the generator with the instancesCount
	"""
	meme_dictionary = {}
	for meme_name in meme_names:
		urlName, instancesCount = get_meme_generator(meme_name)
		meme_dictionary[urlName] = instancesCount
	return meme_dictionary

def get_meme_generator(meme_name):
	"""Queries for a meme generator matching the meme_name. Selects the top ranking (i.e. most memes)
	generator and returns the generator's urlName and instancesCount as well.
	"""
	payload = {'q': meme_name, 'pageIndex': 0, 'pageSize': 24}
	jsonResponse = requests.get(base_gen_uri, params = payload).json()
	top_generator = ''
	top_instances = 0
	for generator in jsonResponse['result']:
		if generator['instancesCount'] > top_instances:
			top_instances = generator['instancesCount']
			top_generator = generator['urlName']
	return (top_generator, top_instances)

def get_memetadata(meme_name, count):
	"""Populates the database with memes
	"""
	meme_type = MemeType.get_or_create(meme_type_name = meme_name)[0]

	for i in range(0, count // 24):
		payload = {'languageCode': 'en', 'pageIndex': i, 'pageSize': 24, 'urlName': meme_name}
		jsonResponse = requests.get(base_data_uri, params = payload).json()
		
		for meme in jsonResponse['result']:
			Meme.create (
				top_text=meme['text0'],
				bottom_text=meme['text1'],
				score=meme['totalVotesScore'],
				meme_type_id=meme_type
			)

if __name__ == '__main__':
	meme_dictionary = None

	if len(sys.argv) == 2 and os.path.exists(sys.argv[1]):
		try:
			with open(sys.argv[1], 'r') as f:
				meme_dictionary = json.load(f)
		except:
			raise
	else:
		meme_dictionary = get_meme_dictionary(meme_names)

		outf = ""
		if len(sys.argv) == 2:
			outf = sys.argv[1]
		else:
			outf = 'meme_dict.json'

		with open(outf, 'w') as f:
			json.dump(meme_dictionary, f)

	for meme, count in meme_dictionary.iteritems():
		get_memetadata(meme, count)
