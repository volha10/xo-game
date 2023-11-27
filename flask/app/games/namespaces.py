from flask_restx import fields, Namespace

from app.games.enums import MarkType, GameResultLabel

games_ns = Namespace("games")

_turn_model = games_ns.model(
    "_Turn",
    {
        "turn_number": fields.Integer(),
        "mark": fields.String(enum=MarkType.list()),
        "position": fields.Integer(),
    },
)

_player_model = games_ns.model(
    "_Player",
    {
        "id": fields.Integer(),
        "mark": fields.String(enum=MarkType.list()),
        "game_result": fields.String(
            enum=GameResultLabel.list(),
        ),
    },
)

game_response_model = games_ns.model(
    "Game",
    {
        "id": fields.Integer(),
        "total_turns": fields.Integer(),
        "turns_overview": fields.List(fields.Nested(_turn_model), default=[]),
        "created_dttm": fields.DateTime,
        "finished_dttm": fields.DateTime,
        "users": fields.List(
            fields.Nested(_player_model),
            example=[
                {"id": 1, "mark": "X", "game_result": None},
                {"id": 2, "mark": "O", "game_result": None},
            ],
        ),
    },
)

new_game_request_model = games_ns.model(
    "NewGame",
    {
        "users": fields.List(
            fields.Nested(_player_model),
            example=[
                {
                    "id": 1,
                    "mark": "X",
                },
                {
                    "id": 2,
                    "mark": "O",
                },
            ],
        )
    },
)
