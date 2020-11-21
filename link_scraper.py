from bs4 import BeautifulSoup
import json
import configparser
import requests
from methods import createSoup, loopOverLinks, loadDictionary
import numpy as np




"""Read configuration from config file."""
config = configparser.ConfigParser()
config.read('config.ini')
BASE_URL = config['DEFAULT']['BASE_URL']
SEASON_PREFIX = config['DEFAULT']['SEASON_PREFIX']
EPISODES_PREFIX = config['DEFAULT']['EPISODES_PREFIX']
DEFAULT_SEASON = config['DEFAULT']['DEFAULT_SEASON']


def getSeasonURL() -> list:
    """
    Given a season number, return the corresponding 
    url for the webpage of said season.
    """
    URL = BASE_URL + DEFAULT_SEASON
    soup = createSoup(URL)

    season_list = loopOverLinks(SEASON_PREFIX, soup)
    season_list.append(DEFAULT_SEASON)
    season_list.reverse()

    return season_list


"""
episodes = loadDictionary('episodes.json')
keylist: list = list(episodes.keys())
keylist.sort()
randomSeason: int = random.randint(keylist[0], keylist[-1])
randomEpisode: int = random.randint(1, episodes[randomSeason])"""




def scrapeSite():

	episodes = set()
	num = 0
	for i in getSeasonURL():
		soup = createSoup(BASE_URL + i)
		for link in soup.find_all('a'):
			l = link.get('href')
			if (l[0:len(EPISODES_PREFIX)] == EPISODES_PREFIX):
				episodes.add(BASE_URL + l)
				num += 1
				if (num > 10):
					num = 0
					soup = createSoup(BASE_URL + l)
					for link in soup.find_all('a'):
						l = link.get('href')
						if (l[0:len(EPISODES_PREFIX)] == EPISODES_PREFIX):
							episodes.add(BASE_URL + l)


	return episodes

#episodes = scrapeSite()
#episodes = np.fromiter(episodes, 'U150' , len(episodes))
#np.savetxt('ALL_EPISODES_UNSORTED.txt', episodes, fmt='%s', delimiter=',')
#print(episodes)

episodes = np.loadtxt('ALL_EPISODES_UNSORTED.txt', dtype="U145")

def sortArray(a: np.ndarray):
	whitelist= set('0 1 2 3 4 5 6 7 8 9')


	sorted = np.copy(a)
	#print(sorted)
	for i, w in enumerate(sorted):
		sorted[i] = ''.join(filter(whitelist.__contains__, w[len(w) - 8:]))
	"""
	for i, w in enumerate(sorted):
		if (len(w) == 2):
			pass
		elif(len(w) == 3):
			sorted[i] = w[0]"""

	print(sorted)
	print(np.sort(sorted.astype(np.int)))
	sorted = sorted.astype(np.int)
	sorted = (np.argsort(sorted))
	print(sorted)

	return sorted

sorted_indexes = sortArray(episodes)
#print(episodes[sorted_indexes])
#print(sortArray(episodes))