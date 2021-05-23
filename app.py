from flask import Flask, request
from flask_restx import Api, Resource

app = Flask(__name__)
api = Api(app, version="1.0", title="XO Game API", description="A simple XO Game API")
ns = api.namespace("xo-games", description="XO Game operations")


@ns.route("/")
class XOGameCreating(Resource):
    def post(self):
        return {
                   "user_id": 1,
                   "user_mark": 1,
                   "board": [[0, 0, 0], [0, 0, 0], [0, 0, 0]]
               }, 201


@ns.route("/<int:game_id>")
class XOGames(Resource):
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

                   ]
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

                   ]
               }, 201
