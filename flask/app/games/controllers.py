from flask import request
from flask_jwt_extended import jwt_required, get_jwt_identity
from flask_restx import Resource

from app.games import namespaces
from app.games import schemas
from app.games import views
from app.games.namespaces import games_ns


@games_ns.route("/")
class NewGame(Resource):

    @jwt_required()
    @games_ns.expect(namespaces.new_game_request_model, validate=True)
    @games_ns.marshal_with(
        namespaces.game_response_model, description="Created", code=201
    )
    def post(self):
        data = request.get_json()
        players = data["users"]

        result = views.create_game(
            schemas.NewGameUserSchema.model_validate(players[0]),
            schemas.NewGameUserSchema.model_validate(players[1]),
        )

        return result.model_dump(), 201


@games_ns.route("/<int:game_id>")
class Games(Resource):

    @jwt_required()
    @games_ns.marshal_with(namespaces.game_board_response_model, code=200)
    def get(self, game_id):
        user_id = get_jwt_identity()
        result = views.get_game(game_id, user_id)

        return result.model_dump(), 200

    @jwt_required()
    @games_ns.expect(namespaces.turn_model, validate=True)
    @games_ns.marshal_with(namespaces.game_board_response_model, code=201)
    def patch(self, game_id):
        turn_user_id = get_jwt_identity()
        turn = request.get_json()

        result = views.make_turn(
            game_id, turn_user_id, schemas.Turn.model_validate(turn)
        )

        return result.model_dump(), 201
