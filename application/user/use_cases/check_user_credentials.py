from application.user.user_repository import UserRepository


class CheckUserCredentials:
    def __init__(self, user_repository: UserRepository):
        self.user_repository = user_repository

    def execute(self, username, password):
        user = self.user_repository.find_by_username_and_password(username, password)
        return user is not None