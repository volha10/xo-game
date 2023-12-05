from flask import Blueprint
from flask_jwt_extended.exceptions import JWTExtendedException
from flask_restx import Api

from app.auth.controllers import auth_ns
from app.auth.views import InvalidEmailOrPasswordError, InvalidOptionError
from app.games.controllers import games_ns
from app.games.views import UpdatingFinishedGameError, GameNotFoundError
from app.management.controllers import management_ns
from app.management.views import NoLeaguesFoundError, OptionNotFoundError

api_v1 = Blueprint("api", __name__, url_prefix="/api/v1")

authorizations = {
    "apikey": {
        "type": "apiKey",
        "in": "header",
        "name": "Authorization"
    }
}

api = Api(
    api_v1,
    version="1.0",
    title="XO Game API",
    description="A simple XO Game API",
    doc="/docs",
    security="apikey",
    authorizations=authorizations
)

api.add_namespace(auth_ns)
api.add_namespace(games_ns)
api.add_namespace(management_ns)


@api.errorhandler(InvalidOptionError)
def handle_invalid_option_error(error):
    return {"message": str(error)}, 400


@api.errorhandler(NoLeaguesFoundError)
def handle_no_leagues_found_error(error):
    return {"message": str(error)}, 400


@api.errorhandler(OptionNotFoundError)
def option_not_found_error(error):
    return {"message": str(error)}, 400


@api.errorhandler(InvalidEmailOrPasswordError)
def handle_invalid_error_or_password_error(error):
    return {"message": str(error)}, 400


@api.errorhandler(GameNotFoundError)
def handle_game_not_found_error(error):
    return {"message": str(error)}, 400


@api.errorhandler(UpdatingFinishedGameError)
def handle_updating_finished_game_error(error):
    return {"message": str(error)}, 400


@api.errorhandler(JWTExtendedException)
def handle_jwt_exceptions(error):
    return {'message': str(error)}, getattr(error, 'code', 401)


@api.errorhandler(Exception)
def handle_unexpected_error(_):
    return {"message": "Internal error"}, 500
