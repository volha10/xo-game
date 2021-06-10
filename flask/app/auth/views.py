import datetime

from flask_jwt_extended import create_access_token

from app import db
from app.auth.models import User

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
