from datetime import datetime
from typing import Optional

from app import db


class League(db.Model):
    __tablename__ = "league"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50))
    started_at = db.Column(db.DateTime, nullable=False)

    def __init__(self, name: str, started_at: Optional[datetime] = None):
        self.name = name
        self.started_at = started_at or datetime.utcnow()


class UserOption(db.Model):
    __tablename__ = "user_option"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=True, nullable=False)
