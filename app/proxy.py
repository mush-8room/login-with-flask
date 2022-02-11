from flask import current_app
from werkzeug.local import LocalProxy

from app.repositories.user import MemUserRepository, DBUserRepository

_repo = None


def get_user_repo():
    global _repo

    if not _repo:
        if current_app.config.get('REPO_TYPE', 'DB') == "DB":
            _repo = DBUserRepository()
        else:
            _repo = MemUserRepository([
                {
                    'id': 1,
                    'email': 'test@test.com',
                    'name': '테스트',
                    'password': 'secret'
                },
            ])

    return _repo


user_repo = LocalProxy(get_user_repo)
