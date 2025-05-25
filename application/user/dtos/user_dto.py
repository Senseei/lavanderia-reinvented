from domain.user import User


class UserDTO:
    def __init__(self, user: User):
        self.id = user.id
        self.username = user.username
        self.name = user.name
        self.cash = user.cash