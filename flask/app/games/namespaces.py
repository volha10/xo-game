from flask_restx import fields, Namespace

from app.games.enums import MarkType, GameResultLabel

games_ns = Namespace("games")


_player_model = games_ns.model(
    "_Player",
    {
        "id": fields.Integer(required=True),
        "mark": fields.String(enum=MarkType.list(), required=True),
        "game_result": fields.String(enum=GameResultLabel.list()),
    },
)

turn_model = games_ns.model(
    "Turn",
    {
        "turn_number": fields.Integer(
            example=1,
            required=True,
            min=1,
            max=9,
        ),
        "mark": fields.String(
            enum=MarkType.list(),
            required=True,
        ),
        "position": fields.Integer(
            example=1,
            required=True,
            min=1,
            max=9,
        ),
    },
)

game_board_response_model = games_ns.model(
    "GameBoard",
    {
        "id": fields.Integer(),
        "total_turns": fields.Integer(),
        "turns_overview": fields.List(fields.Nested(turn_model), default=[]),
        "created_dttm": fields.DateTime,
        "finished_dttm": fields.DateTime,
    },
)

game_response_model = games_ns.model(
    "Game",
    {
        "id": fields.Integer(),
        "total_turns": fields.Integer(),
        "turns_overview": fields.List(fields.Nested(turn_model), default=[]),
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
            required=True,
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

user_games_response_model = games_ns.model(
    "UserGames", {"games": fields.List(fields.Nested(game_response_model))}
)
