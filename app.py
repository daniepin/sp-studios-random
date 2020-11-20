from flask.templating import render_template_string
import methods
from flask import Flask, redirect
import webbrowser

app = Flask(__name__)

@app.route('/')
def index():
    methods.useless()
    season, episode = methods.getRandomSeasonAndEpisode()
    print("Loading S%dE%d" % (season, episode))
    url = methods.getEpisodeURL(season, episode)
    print("Episode url is: {}".format(url))
    # return redirect("https://google.com", code=302)
    webbrowser.open_new_tab(url)
    return redirect(url, code=302)
    return ('', 204)

if __name__ == '__main__':
    # Threaded option to enable multiple instances for multiple user access support
    app.run(threaded=True, port=5000)
