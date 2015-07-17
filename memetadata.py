"""Requests meme metadata (memetadata) from memegenerator's API
"""

import requests

base_data_uri = "http://version1.api.memegenerator.net/Instances_Select_ByNew"

meme_name_dictionary = {'Y-U-No': 2287719, 'Futurama-Fry': 1461840, 'Success-Kid': 1190989,
                        'The-Most-Interesting-Man-In-The-World': 1239075, 'Willywonka': 985064,
                        'Philosoraptor': 733671, 'One-Does-Not-Simply-A': 1146447,
                        'Bad-Luck-Brian-Meme': 653934, 'Good-Guy-Greg': 338941}

for meme, count in meme_name_dictionary.iteritems():
	get_memetadata(meme, count)

def get_memetadata(meme_name, count):

	for i in range(0, count/24):
		payload = {'languageCode': 'en', 'pageIndex': i, 'pageSize': 24, 'urlName': meme_name}
		jsonResponse = requests.get(base_data_uri, params = payload).json()

		"""parse the JSON and write to DB or something here"""