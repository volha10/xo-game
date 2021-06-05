from flask import request
from flask_restx import Resource, fields, Namespace

from app.games.enums import MarkType, GameResultType

games_ns = Namespace("games")


new_game_model_request = games_ns.model("NewGameRequest", {
    "user_id": fields.Integer(required=True)
})

_turn_overview_model = games_ns.model("_TurnOverview", {
    "turn_number": fields.Integer(),
    "mark": fields.String(enum=MarkType.list()),
    "position": fields.Integer()
})

game_model_response = games_ns.model("GameResponse", {
    "id": fields.Integer(),
    "user_id": fields.Integer(),
    "user_mark": fields.String(enum=MarkType.list()),
    "result": fields.String(enum=GameResultType.list()),
    "total_turns": fields.Integer(),
    "overview": fields.List(fields.Nested(_turn_overview_model), default=[]),
    "started_dttm": fields.DateTime,
    "finished_dttm": fields.DateTime,

})

user_turn_model_request = games_ns.model("UserTurnModelRequest", {
    "turn_number": fields.Integer(),
    "position": fields.Integer()
})


from app.games import views


@games_ns.route("/")
class NewGame(Resource):

    @games_ns.expect(new_game_model_request, validate=True)
    @games_ns.marshal_with(game_model_response, description="Created", code=201)
    def post(self):
        data = request.get_json()
        user_id = data.get("user_id")

        return views.create_game(user_id), 201


@games_ns.route("/<int:game_id>")
class Games(Resource):

    @games_ns.marshal_with(game_model_response, code=200)
    def get(self, game_id):
        return views.get_game(game_id), 200

    @games_ns.expect(user_turn_model_request)
    @games_ns.marshal_with(game_model_response, code=201)
    def patch(self, game_id):
        turn_overview = request.get_json()
        return views.make_turn(game_id, turn_overview), 201
