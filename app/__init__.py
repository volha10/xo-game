from flask import Flask
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy


db = SQLAlchemy()
migrate = Migrate()


def create_app(app_config):
    app = Flask(__name__, instance_relative_config=True)

    print(app_config)
    app.config.from_object(app_config)

    db.init_app(app)
    migrate.init_app(app, db)

    from app.api_v1 import api_v1

    app.register_blueprint(api_v1)
    return app
