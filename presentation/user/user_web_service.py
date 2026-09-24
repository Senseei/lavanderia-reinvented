from application.user.usecases.user_service import UserService
from presentation.auth.dtos.authenticated_user_dto import AuthenticatedUserDTO


class UserWebService:
    def __init__(self, user_service: UserService):
        self._user_service = user_service

    def find_session_user(self, user_id: int) -> AuthenticatedUserDTO:
        return AuthenticatedUserDTO(self._user_service.find_by_id(user_id))
