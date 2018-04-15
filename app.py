from flask import Flask
from main import TrumpBot
application = Flask(__name__)

@application.route("/")
def hello():
    return TrumpBot.generate_speech()

if __name__ == "__main__":
    application.run(host="0.0.0.0")
