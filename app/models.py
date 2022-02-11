from sqlalchemy import Column, Integer, Unicode

from app.database import db


class UserEntity:
    def __init__(self, id, email, name, password):
        self.id = id
        self.email = email
        self.name = name
        self.password = password

    @property
    def is_authenticated(self):
        return True

    @property
    def is_active(self):
        return True

    @property
    def is_anonymous(self):
        return True

    def get_id(self):
        return self.id

    def __repr__(self):
        return f"<User:{self.id}>"


class User(db.Model):
    __tablename__ = "users"

    id = Column("id", Integer, primary_key=True)
    name = Column("name", Unicode, nullable=False)
    email = Column("email", Unicode, nullable=False, unique=True)
    password = Column(
        "password", Unicode, nullable=False, server_default=""
    )
