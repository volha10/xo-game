from flask import request
from flask_restx import Resource, fields, Namespace


games_ns = Namespace("games")


new_game_model_request = games_ns.model("NewGameRequest", {
    "user_id": fields.Integer(required=True)
})

step_model = games_ns.model("TurnOverviewModel", {
    "turn_number": fields.Integer(),
    #"mark": fields.Integer(),
    "position": fields.Integer()
})

game_model_response = games_ns.model("GameResponse", {
    "id": fields.Integer(),
    "user_id": fields.Integer(),
    "user_mark": fields.String(max_length=1, ),  # TODO: fields.Integer(),
    "result": fields.String(max_length=1),  # TODO: fields.Integer(),
    "total_turns": fields.Integer(),
    "overview": fields.List(fields.Nested(step_model)),
    "started_dttm": fields.DateTime,
    "finished_dttm": fields.DateTime,

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

    @games_ns.expect(step_model)
    @games_ns.marshal_with(game_model_response, code=201)
    def patch(self, game_id):
        # data = request.get_json()
        turn_overview = {
                   "turn_number": 1,
                   #"mark": 1,  # x=1 or 0=2
                   "position": 5
        }

        return views.make_turn(game_id, turn_overview), 201
