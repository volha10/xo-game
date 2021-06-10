from flask_bcrypt import generate_password_hash, check_password_hash

from app import db


class User(db.Model):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(60), nullable=False)

    def __init__(self, name: str, email: str, password: str):
        self.name = name
        self.email = email
        self.password = generate_password_hash(password).decode("utf8")

    def __repr__(self):
        return "User %s" % self.id

    def check_password(self, password: str) -> bool:
        """
        Check if password used by user to login is equal to the password
        saved in the database.
        """
        return check_password_hash(self.password, password)
