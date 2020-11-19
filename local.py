import methods

def index():
    season, episode = methods.getRandomSeasonAndEpisode()
    print("Loading S%dE%d" % (season, episode))
    url = methods.getEpisodeURL(season, episode)
    print("Episode url is: {}".format(url))
    methods.launcher('firefox', url)
    print("Episode loaded!")

if __name__ == '__main__':
    index()