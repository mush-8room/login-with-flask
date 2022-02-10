user_pool = [
    {
        'id': 1,
        'email': 'test@test.com',
        'name': '테스트',
        'password': 'secret'
    },
]


class User:
    # id
    # email
    # name
    # password
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
