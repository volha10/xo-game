from flask import request
from flask_jwt_extended import jwt_required, get_jwt_identity
from flask_restx import Resource

from app.games import views
from app.games.namespaces import (
    games_ns,
    game_model_response,
    user_turn_model_request
)


@games_ns.route("/")
class NewGame(Resource):

    @jwt_required()
    @games_ns.marshal_with(game_model_response, description="Created", code=201)
    def post(self):
        user_id = get_jwt_identity()
        return views.create_game(user_id), 201


@games_ns.route("/<int:game_id>")
class Games(Resource):

    @jwt_required()
    @games_ns.marshal_with(game_model_response, code=200)
    def get(self, game_id):
        user_id = get_jwt_identity()
        return views.get_game(game_id, user_id), 200

    @jwt_required()
    @games_ns.expect(user_turn_model_request)
    @games_ns.marshal_with(game_model_response, code=201)
    def patch(self, game_id):
        user_id = get_jwt_identity()
        turn_overview = request.get_json()

        return views.make_turn(game_id, turn_overview, user_id), 201
