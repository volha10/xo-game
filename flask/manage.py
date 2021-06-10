import os

from app import create_app

app = create_app(os.environ["APP_CONFIG"])


if __name__ == "__main__":
    app.run()
