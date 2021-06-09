from flask.cli import FlaskGroup

import os

from app import create_app

app = create_app(os.environ["APP_CONFIG"])


if __name__ == "__main__":
    #app.run(host="0.0.0.0")
    app.run()
