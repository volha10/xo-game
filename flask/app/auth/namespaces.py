from flask_restx import Namespace, fields

auth_ns = Namespace("auth")

signup_request_model = auth_ns.model(
    "SignupRequest",
    {
        "name": fields.String(required=True),
        "email": fields.String(required=True),
        "password": fields.String(required=True, min_length=6),
    },
)

signup_response_model = auth_ns.model(
    "SignupResponse", {"id": fields.Integer(required=True)}
)

login_request_model = auth_ns.model(
    "LoginRequest",
    {"email": fields.String(required=True), "password": fields.String(required=True)},
)

login_response_model = auth_ns.model(
    "LoginResponse", {"access_token": fields.String(required=True)}
)


user_options_request_model = auth_ns.model(
    "NewUserOptionsRequest", {
        'options': fields.Raw(required=True)
    }
)


