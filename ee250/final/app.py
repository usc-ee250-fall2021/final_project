# Flask application libraries:
from flask import Flask
from flask import send_from_directory, abort

# Flask application implementation:
app = Flask(__name__)
# @app.route("/get-audio/<string:audio_name>")
# def get_audio(audio_name):
#     print(audio_name)
#     return "Thanks"

@app.route("/")
def index():
    return "Hello world!"


if __name__ == "__main__":
    app.run()