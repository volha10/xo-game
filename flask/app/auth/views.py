import datetime
from typing import List

from flask_jwt_extended import create_access_token

from app import db
from app.auth import schemas
from app.auth.models import User
from app.management.models import UserOption

JWT_EXPIRES_DELTA = 7


class InvalidEmailOrPasswordError(Exception):
    pass


class InvalidOptionError(Exception):
    pass


def create_user(name: str, email: str, password: str) -> User:
    user = User(name=name, email=email, password=password)

    db.session.add(user)
    db.session.commit()

    return user


def login(email: str, password: str) -> str:
    user = User.query.filter_by(email=email).first()

    if not user:
        raise InvalidEmailOrPasswordError("Invalid email or password.")

    authorized = user.check_password(password)

    if not authorized:
        raise InvalidEmailOrPasswordError("Invalid email or password.")

    expires = datetime.timedelta(days=JWT_EXPIRES_DELTA)
    return create_access_token(identity=str(user.id), expires_delta=expires)


def get_user(user_id: int) -> schemas.UserSchema:
    user = User.query.filter_by(id=user_id).one()
    schema = _populate_options(user)

    return schema


def get_users() -> schemas.UsersSchema:
    users = User.query.all()
    user_schema_list = [schemas.UserLink.model_validate(user) for user in users]
    result = schemas.UsersSchema(users=user_schema_list)

    return result


def set_options(user_id: int, options: dict) -> schemas.UserSchema:
    _check_options(options)

    user = User.query.filter_by(id=user_id).first()
    user.profile_options = options

    db.session.add(user)
    db.session.commit()

    schema = _populate_options(user)

    return schema


def _get_available_option_names() -> List[str]:
    available_options = UserOption.query.with_entities(UserOption.name).all()
    available_options_list = []

    if available_options:
        available_options_list = [option[0] for option in available_options]

    return available_options_list


def _check_options(options) -> None:
    available_options_list = _get_available_option_names()

    for option in options:
        if option not in available_options_list:
            raise InvalidOptionError("Option %s is invalid." % option)


def _populate_options(user) -> schemas.UserSchema:
    available_options_list = _get_available_option_names()

    schema = schemas.UserSchema.model_validate(user)
    schema.available_option_list = available_options_list

    return schema
