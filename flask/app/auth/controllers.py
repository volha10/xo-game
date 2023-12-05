from flask import request
from flask_jwt_extended import jwt_required, get_jwt_identity
from flask_restx import Resource

from app.auth import views as users_views
from app.auth.namespaces import (
    auth_ns,
    signup_request_model,
    signup_response_model,
    login_request_model,
    login_response_model,
    user_options_request_model,
)


@auth_ns.route("/signup")
class SignUp(Resource):
    @auth_ns.expect(signup_request_model, validate=True)
    @auth_ns.marshal_with(signup_response_model, description="Created", code=201)
    def post(self):
        data = request.get_json()
        return users_views.create_user(**data), 201


@auth_ns.route("/login")
class Login(Resource):
    @auth_ns.expect(login_request_model)
    @auth_ns.marshal_with(login_response_model, description="Accepted", code=200)
    def post(self):
        data = request.get_json()
        return {"access_token": users_views.login(**data)}, 200


@auth_ns.route("/<int:user_id>")
class UserId(Resource):
    def get(self, user_id: int):
        result = users_views.get_user(user_id)
        return result.model_dump(), 200


@auth_ns.route("")
class User(Resource):
    @jwt_required()
    @auth_ns.expect(user_options_request_model, validate=True)
    def patch(self):
        user_id = get_jwt_identity()
        payload = request.get_json()
        options = payload.get('options')

        result = users_views.set_options(
            user_id, options
        )

        return result.model_dump(), 200
