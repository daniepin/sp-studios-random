import random
import requests
from bs4 import BeautifulSoup
import webbrowser
import configparser
import json


def createConfigFile() -> None:
    """ Creates a config file with a defualt case """
    config = configparser.ConfigParser()
    config['DEFAULT'] = {'BASE_URL': "https://www.southparkstudios.nu",
                         'SEASON_PREFIX': "/seasons/south-park/",
                         'EPISODES_PREFIX': "/episodes/",
                         'DEFAULT_SEASON': "/seasons/south-park/yjy8n9/season-1"}
    with open('config.ini', 'w') as config_file:
        config.write(config_file)


# createConfigFile()

"""Read configuration from config file."""
config = configparser.ConfigParser()
config.read('config.ini')
BASE_URL = config['DEFAULT']['BASE_URL']
SEASON_PREFIX = config['DEFAULT']['SEASON_PREFIX']
EPISODES_PREFIX = config['DEFAULT']['EPISODES_PREFIX']
DEFAULT_SEASON = config['DEFAULT']['DEFAULT_SEASON']

def useless():
    print("Params loaded from config.ini")
    print(BASE_URL)
    print(SEASON_PREFIX)
    print(EPISODES_PREFIX)
    print(DEFAULT_SEASON)
    print("---------End-----------")


def loadDictionary(filename: str) -> dict:
    """ 
    Loads a dictionary from JSON file and converts keys
    from str to int.  
    """
    with open(filename) as f:
        data: str = f.read()
        episodes: dict = json.loads(data)
        episodes = {int(k): v for k, v in episodes.items()}
    return episodes


def getRandomSeasonAndEpisode() -> int:
    """ 
    Return a random season number and a random episode
    within current season.
    """
    episodes = loadDictionary('episodes.json')
    keylist: list = list(episodes.keys())
    keylist.sort()
    randomSeason: int = random.randint(keylist[0], keylist[-1])
    randomEpisode: int = random.randint(1, episodes[randomSeason])

    return randomSeason, randomEpisode


def createSoup(url: str) -> BeautifulSoup:
    """ Return a BeutifulSoup object of website located at url"""
    page = requests.get(url)
    #print("url:", url)
    #print("page content", page.content)
    #s = BeautifulSoup(page.content, 'html.parser')
    #print(s.prettify())
    return BeautifulSoup(page.content, 'html.parser')


def loopOverLinks(condition: str, soup: BeautifulSoup, extra_str: str = "") -> list:
    """ 
    Iterate over a BeautifulSoup object looking for all 'a' tags that 
    satisfy some condition.
    """
    list_ = []
    print("condition =", condition)
    print("--------------------------------------------------")
    for link in soup.find_all('a'):
        l = link.get('href')
        print(l)
        if (l[0:len(condition)] == condition):
            list_.append(extra_str + l)

    print("--------------------------------------------------")
    return list_


def getSeasonURL(seasonNum: int) -> str:
    """
    Given a season number, return the corresponding 
    url for the webpage of said season.
    """
    URL = BASE_URL + DEFAULT_SEASON
    soup = createSoup(URL)

    season_list = loopOverLinks(SEASON_PREFIX, soup)
    season_list.append(DEFAULT_SEASON)
    season_list.reverse()

    return season_list[seasonNum - 1]


def getEpisodeURL(season: int, episode: int) -> str:
    """
    Given a season and episode number, return the corresponding 
    url for the webpage of said episode.
    """
    URL = BASE_URL + getSeasonURL(season)
    print("In getEpisodeURL: url =", URL)

    soup = createSoup(URL)
    episode_list = loopOverLinks(EPISODES_PREFIX, soup, BASE_URL)
    print("episode_list length: {}\n EPISODES_PREFIX:  {}\nBASE_URL: {} ||".format(len(episode_list), EPISODES_PREFIX, BASE_URL))

    """ 
    This check is needed because if an episode number is
    bigger than 10, it will not show up on the page for a 
    given season, so we have to do a little trick instead
    to fetch the correct adress.     
    """
    if (episode > 10):
        temp_url = episode_list[-1]
        soup = createSoup(temp_url)
        episode_list = loopOverLinks(EPISODES_PREFIX, soup, BASE_URL)

        return episode_list[10 + (episode - 10)]

    if (len(episode_list) == 0):
        print("Season %d does not contain any episodes! Please try again." % season)
        exit(0)

    return episode_list[episode - 1]


def launcher(browser: str, url: str) -> None:
    """ Launch a browser window in a new tab. """
    webbrowser.register(browser, None)
    webbrowser.get().open(url)



