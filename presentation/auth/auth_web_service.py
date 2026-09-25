from application.auth.usecases.auth_service import AuthService
from presentation.auth.dtos.authenticated_user_dto import AuthenticatedUserDTO
from presentation.auth.dtos.login_credentials_dto import LoginCredentialsDTO
from presentation.auth.dtos.new_user_dto import NewUserDTO
from presentation.user.dtos.user_dto import UserDTO
from di.decorators import component


@component
class AuthWebService:
    def __init__(self, auth_service: AuthService):
        self._auth_service = auth_service

    def login(self, credentials: LoginCredentialsDTO) -> AuthenticatedUserDTO:
        return AuthenticatedUserDTO(self._auth_service.login(credentials.username, credentials.password))

    def register(self, dto: NewUserDTO) -> UserDTO:
        return UserDTO(self._auth_service.register(dto.username, dto.name, dto.password))
