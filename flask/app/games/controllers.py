from flask import request
from flask_restx import Resource

from app.games import schemas
from app.games import views
from app.games.namespaces import (
    games_ns,
    new_game_request_model,
    game_response_model,
)


@games_ns.route("/")
class NewGame(Resource):
    @games_ns.expect(new_game_request_model)
    @games_ns.marshal_with(game_response_model, description="Created", code=201)
    def post(self):
        data = request.get_json()
        players = data["users"]

        result = views.create_game(
            schemas.NewGameUserSchema.model_validate(players[0]),
            schemas.NewGameUserSchema.model_validate(players[1]),
        )

        return result.model_dump(), 201
