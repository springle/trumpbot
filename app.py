from flask import Flask
from main import TrumpBot
application = Flask(__name__)

# Trigger matrix generation
print("Starting matrix generation")
TrumpBot.generate_speech()
print("Finished matrix generation")

@application.route("/")
def hello():
    return TrumpBot.generate_speech()

if __name__ == "__main__":
    application.run(host="0.0.0.0")
