from flask.templating import render_template_string
import methods
from flask import Flask, render_template
import requests

app = Flask(__name__)

@app.route('/')
def index():
    season, episode = methods.getRandomSeasonAndEpisode()
    print("Loading S%dE%d" % (season, episode))
    url = methods.getEpisodeURL(season, episode)
    print("Episode url is: {}".format(url))
    # methods.launcher('firefox', url)
    print("Episode loaded!")
    html = requests.get(url)
    return render_template_string(html.text)

if __name__ == '__main__':
    # Threaded option to enable multiple instances for multiple user access support
    app.run(threaded=True, port=5000)
