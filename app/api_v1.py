from flask import Blueprint
from flask_restx import Api

from app.games.controllers import games_ns

api_v1 = Blueprint("api", __name__, url_prefix="/api/v1")

api = Api(api_v1, version="1.0", title="XO Game API", description="A simple XO Game API", doc="/docs")

api.add_namespace(games_ns)
