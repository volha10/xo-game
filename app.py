import os

from flask import Flask
from flask_migrate import Migrate
from flask_restx import Api, Resource
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config.from_object(os.environ["APP_SETTINGS"])

db = SQLAlchemy(app)
migrate = Migrate(app, db)

api = Api(app, version="1.0", title="XO Game API", description="A simple XO Game API")
ns = api.namespace("games", description="XO Game operations")

from models import User, Game


@ns.route("/")
class GameCreating(Resource):
    def post(self):
        return {
                   "user_id": 1,
                   "user_mark": 1,
                   "board": [[0, 0, 0], [0, 0, 0], [0, 0, 0]]
               }, 201


@ns.route("/<int:game_id>")
class Games(Resource):
    def get(self, game_id):
        return {
                   "game_id": game_id,
                   "user_id": 1,
                   "user_mark": 1,
                   "result": None,
                   "overview": [
                       {
                           "step": 1,
                           "mark": 1,
                           "position": {"x": 1, "y": 1}
                       },
                       {
                           "step": 2,
                           "mark": 2,
                           "position": {"x": 0, "y": 2}
                       },
                   ],
                   "started_dttm": "2021-02-23 00:00:00",
                   "finished_dttm": None,
               }, 200

    def patch(self, game_id):
        # data = request.get_json()
        data = {
                   "step": 1,
                   "mark": 1,  # x=1 or 0=2
                   "position": {"x": 1, "y": 1}
               },

        return {
                   "game_id": game_id,
                   "user_id": 1,
                   "user_mark": 1,
                   "result": None,
                   "overview": [
                       {
                           "step": 1,
                           "mark": 1,
                           "position": {"x": 1, "y": 1}
                       },
                       {
                           "step": 2,
                           "mark": 2,
                           "position": {"x": 0, "y": 2}
                       },
                   ],
                   "started_dttm": "2021-02-23 00:00:00",
                   "finished_dttm": None,
               }, 201
