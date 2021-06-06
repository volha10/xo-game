from flask_restx import fields, Namespace

from app.games.enums import MarkType, GameResultType

games_ns = Namespace("games")


_turn_overview_model = games_ns.model("_TurnOverview", {
    "turn_number": fields.Integer(),
    "mark": fields.String(enum=MarkType.list()),
    "position": fields.Integer()
})

game_model_response = games_ns.model("GameResponse", {
    "id": fields.Integer(),
    "user_id": fields.Integer(),
    "user_mark": fields.String(enum=MarkType.list()),
    "result": fields.String(enum=GameResultType.list()),
    "total_turns": fields.Integer(),
    "overview": fields.List(fields.Nested(_turn_overview_model), default=[]),
    "started_dttm": fields.DateTime,
    "finished_dttm": fields.DateTime,

})

user_turn_model_request = games_ns.model("UserTurnModelRequest", {
    "turn_number": fields.Integer(),
    "position": fields.Integer()
})
