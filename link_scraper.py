<<<<<<< HEAD
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


def getKeyAndEps():
    episodes = loadDictionary('episodes.json')
    keylist: list = list(episodes.keys())
    keylist.sort()

    return keylist, episodes


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
#episodes.add('https://www.southparkstudios.nu/episodes/7rd3vw/south-park-a-very-crappy-christmas-season-4-ep-17')
#episodes = np.fromiter(episodes, 'U150' , len(episodes))
#print(len(episodes))
#np.savetxt('ALL_EPISODES_UNSORTED.txt', episodes, fmt='%s', delimiter=',')

episodes = np.loadtxt('ALL_EPISODES_UNSORTED.txt', dtype="U145")


def sortSection(a: np.ndarray, copy: np.ndarray, sorted: np.ndarray, n: int, seasonal_eps: np.ndarray):
    if (n == 0):
        indexes = [0]
        prev_sum = 0
    else:
        indexes = np.arange(0, n, 1)
        prev_sum = np.sum(seasonal_eps[indexes])

    if (len(a) < 307 and n == 3):
        seasonal_eps[n] -= 1

    s = [w[w.index("ep") + 2:] for i, w in enumerate(sorted) if (i >= prev_sum and i < seasonal_eps[n] + prev_sum)]
    s = np.array(s)
    s_args = np.argsort(s.astype(np.int)) + prev_sum

    for i in range(prev_sum, prev_sum + seasonal_eps[n]):
        a[i] = copy[s_args[i - prev_sum]]


    return a

def sortArray(a: np.ndarray):
    whitelist = set('0 1 2 3 4 5 6 7 8 9 ep')

    sorted = np.ndarray.copy(a)
    seasons = np.ndarray.copy(a)

    for i, w in enumerate(sorted):
        sorted[i] = ''.join(filter(whitelist.__contains__, w[len(w) - 8:]))

    for i, w in enumerate(sorted):
        seasons[i] = w[:w.index("ep")]

    keylist, ep = getKeyAndEps()
    seasonal_eps = np.zeros(len(keylist), dtype=np.int)

    for k in range(len(keylist)):
        seasonal_eps[k] = ep[keylist[k]]

    seasons_args = np.argsort(seasons.astype(np.int))
    a = a[seasons_args]
    sorted_copy = np.ndarray.copy(a)

    for i in range(0, len(keylist)):
        a = sortSection(a, sorted_copy, sorted[seasons_args], i, seasonal_eps)

    return a

#np.savetxt('ALL_EPISODES_SORTED.txt', sortArray(episodes), fmt='%s', delimiter=',')
=======
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
>>>>>>> main
