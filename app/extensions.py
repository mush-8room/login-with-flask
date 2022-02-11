from flask_login import LoginManager

from app.proxy import user_repo

login_manager = LoginManager()


@login_manager.user_loader
def load_user(user_id):
    return user_repo.get(user_id)

    # target_user = None
    # for user in user_pool:
    #     if user.get('id') == user_id:
    #         target_user = user
    #
    # if target_user:
    #     return User(target_user.get('id'), target_user.get('email'), target_user.get('name'),
    #                 target_user.get('password'))
