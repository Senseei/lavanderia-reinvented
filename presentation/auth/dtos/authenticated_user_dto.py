from application.util.currency import br
from domain.user import User


class AuthenticatedUserDTO:
    def __init__(self, user: User):
        self.id = user.id
        self.name = user.name
        self.cash = user.cash

    def get_formatted_cash(self) -> str:
        return br(self.cash)