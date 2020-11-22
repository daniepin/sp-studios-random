import methods
from flask import Flask, redirect

app = Flask(__name__)

@app.route('/')
def index():
    url = methods.getRandomEpisode()
    print("Episode url is: {}".format(url))
    return redirect(url, code=302)

if __name__ == '__main__':
    # Threaded option to enable multiple instances for multiple user access support
    app.run(threaded=True, port=5000)
