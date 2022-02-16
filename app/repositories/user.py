import abc

from app.models import User
from app.domain.user import UserEntity
from app.database import db


class BaseUserRepository(abc.ABC):

    @abc.abstractmethod
    def get(self, user_id):
        raise NotImplementedError

    @abc.abstractmethod
    def get_by_username(self, username):
        raise NotImplementedError

    @abc.abstractmethod
    def list(self, ):
        raise NotImplementedError


class MemUserRepository(BaseUserRepository):
    def get_by_username(self, username):
        target_user = None
        for user in self.data:
            if user.get('email') == username:
                target_user = user

        if target_user:
            return UserEntity(
                target_user.get('id'),
                target_user.get('email'),
                target_user.get('name'),
                target_user.get('password'))

    def __init__(self, initial_data):
        self.data = initial_data

    def get(self, user_id):
        target_user = None
        for user in self.data:
            if user.get('id') == user_id:
                target_user = user

        if target_user:
            return UserEntity(
                target_user.get('id'),
                target_user.get('email'),
                target_user.get('name'),
                target_user.get('password'))

    def list(self):
        pass


class DBUserRepository(BaseUserRepository):
    def get(self, user_id):
        user = db.session.query(User).get(user_id)
        if user:
            return UserEntity(
                user.id,
                user.email,
                user.name,
                user.password,
            )

    def get_by_username(self, username):
        user = db.session.query(User).filter(User.email == username).first()
        if user:
            return UserEntity(
                user.id,
                user.email,
                user.name,
                user.password,
            )

    def list(self):
        pass
