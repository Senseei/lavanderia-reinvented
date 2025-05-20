from adapters.user.dtos.login_credentials_dto import LoginCredentialsDTO
from adapters.user.dtos.login_response_dto import LoginResponseDTO
from application.errors.entity_not_found_error import EntityNotFoundError
from application.user.use_cases.auth_service import AuthService


class AuthControllerAdapter:
    def __init__(self, auth_service: AuthService):
        self._auth_service = auth_service

    def login(self, credentials_dict) -> LoginResponseDTO:
        credentials = LoginCredentialsDTO.from_dict(credentials_dict)

        if not credentials:
            return LoginResponseDTO(success=False, message="Invalid credentials")

        try:
            user = self._auth_service.login(credentials.username, credentials.password)
            return LoginResponseDTO.success_response(user)
        except EntityNotFoundError as e:
            return LoginResponseDTO.error_response(str(e))