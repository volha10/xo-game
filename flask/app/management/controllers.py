from flask import request
from flask_restx import Resource

from app.management import schemas
from app.management import views, namespaces
from app.management.namespaces import management_ns


@management_ns.route("/leagues/")
class Leagues(Resource):
    @management_ns.expect(namespaces.new_league_request_model, validate=True)
    @management_ns.marshal_with(
        namespaces.league_response_model, description="Created", code=201
    )
    def post(self):
        data = request.get_json()
        result = views.start_league(schemas.LeagueCreate.model_validate(data))

        return result, 201


@management_ns.route("/user-rating")
class UserRating(Resource):
    @management_ns.marshal_with(namespaces.rank_table_response_model, code=200)
    def get(self):
        result = views.get_rank_table()

        return result.model_dump(), 200
