from flask import request
from flask_restx import Resource

from app.auth import views as users_views
from app.management import schemas
from app.management import views, namespaces
from app.management.namespaces import management_ns


@management_ns.route("/leagues")
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


@management_ns.route("/users")
class UserList(Resource):
    @management_ns.marshal_with(namespaces.users_response_model, code=200)
    def get(self):
        result = users_views.get_users()

        return result.model_dump(), 200


@management_ns.route("/options")
class Options(Resource):
    @management_ns.expect(namespaces.new_option_request_model, validate=True)
    @management_ns.marshal_with(
        namespaces.option_response_model, description="Created", code=201
    )
    def post(self):
        data = request.get_json()
        result = views.add_option(schemas.OptionCreate.model_validate(data))

        return result, 201

    @management_ns.marshal_with(namespaces.options_response_model, code=200)
    def get(self):
        result = views.get_options()

        return {"options": result}, 200


@management_ns.route("/options/<int:option_id>")
class Option(Resource):
    @management_ns.response(204, description="Deleted")
    def delete(self, option_id: int):
        views.delete_option(option_id)

        return {"message": "Deleted"}, 204
