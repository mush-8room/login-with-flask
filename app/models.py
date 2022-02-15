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

    # @property
    # def is_active(self):
    #     return True

    def to_entity(self):
        return UserEntity(
            id=self.id, name=self.name, email=self.email, password=self.password
        )


class Connection(db.Model):
    id = db.Column(db.Integer, primary_key=True)

    user_id = db.Column(db.Integer, db.ForeignKey(User.id))
    user = db.relationship('User', backref="connections")
    # addresses = db.relationship('Address', backref='person', lazy=True)

    provider_id = db.Column(db.String(255))
    provider_user_id = db.Column(db.String(255))
    access_token = db.Column(db.String(255))
    secret = db.Column(db.String(255))
    display_name = db.Column(db.String(255))
    profile_url = db.Column(db.String(512))
    image_url = db.Column(db.String(512))
