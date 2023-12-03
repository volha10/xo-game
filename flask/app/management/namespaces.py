from flask_restx import fields, Namespace

management_ns = Namespace("management")

new_league_request_model = management_ns.model(
    "NewLeague", {"name": fields.String(required=True, max_length=50)}
)


league_response_model = management_ns.model(
    "League",
    {
        "id": fields.Integer(required=True),
        "name": fields.String(required=True, max_length=50),
        "started_at": fields.DateTime(required=True),
    },
)

user_rank = management_ns.model(
    "UserRank",
    {
        "rank_number": fields.Integer(),
        "user_id": fields.Integer(),
        "total_result": fields.Integer(),
    },
)

rank_table_response_model = management_ns.model(
    "RankTable",
    {"rank_table": fields.List(fields.Nested(user_rank))},
)
