
from flask import Flask, request
import pages

app = Flask(__name__)

app.register_blueprint(pages.pages)


if __name__ == "__main__":
    app.debug = True
    app.run(host='0.0.0.0', threaded=True)

