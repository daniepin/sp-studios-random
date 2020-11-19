import methods
import os
from flask import Flask, redirect

app = Flask(__name__)

@app.route('/')
def hello():
    season, episode = methods.getRandomSeasonAndEpisode()
    print("Loading S%dE%d" % (season, episode))
    url = methods.getEpisodeURL(season, episode)
    print("Episode url is: {}".format(url))
    # methods.launcher('firefox', url)
    print("Episode loaded!")
    return redirect(url, code=302)

if __name__ == '__main__':
    # Bind to PORT if defined, otherwise default to 5000.
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
