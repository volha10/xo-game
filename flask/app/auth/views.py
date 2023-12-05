import datetime

from flask_jwt_extended import create_access_token

from app import db
from app.auth import schemas
from app.auth.models import User
from app.management.models import UserOption

JWT_EXPIRES_DELTA = 7


class InvalidEmailOrPasswordError(Exception):
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
    options = UserOption.query.with_entities(UserOption.name).all()

    available_options_list = []
    if options:
        available_options_list = [option[0] for option in options]

    schema = schemas.UserSchema.model_validate(user)
    schema.available_option_list = available_options_list
    return schema


def get_users() -> schemas.UsersSchema:
    users = User.query.all()
    user_schema_list = [schemas.UserLink.model_validate(user) for user in users]
    result = schemas.UsersSchema(users=user_schema_list)

    return result
