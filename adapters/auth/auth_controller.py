from adapters.auth.dtos.login_credentials_dto import LoginCredentialsDTO
from adapters.dtos.request_dto import RequestDTO
from adapters.dtos.response_dto import ResponseDTO
from application.auth.dtos.authenticated_user_dto import AuthenticatedUserDTO
from application.auth.dtos.new_user_dto import NewUserDTO
from application.errors.invalid_credentials_error import InvalidCredentialsError
from application.user.dtos.user_dto import UserDTO
from application.errors.duplicate_entity_error import DuplicateEntityError
from application.auth.usecases.auth_service import AuthService


class AuthControllerAdapter:
    def __init__(self, auth_service: AuthService):
        self._auth_service = auth_service

    def login(self, request: RequestDTO) -> ResponseDTO[AuthenticatedUserDTO]:
        credentials = LoginCredentialsDTO.from_dict(request.body)

        if not credentials:
            return ResponseDTO(success=False, message="Invalid credentials")

        try:
            user = self._auth_service.login(credentials.username, credentials.password)
            return ResponseDTO.success_response(user)
        except InvalidCredentialsError as e:
            return ResponseDTO.error_response(str(e))

    def register(self, request: RequestDTO) -> ResponseDTO[UserDTO]:
        dto = NewUserDTO.from_dict(request.body)

        if not dto:
            return ResponseDTO(success=False, message="There are missing fields! Please, fill each one of them.")

        try:
            new_user = self._auth_service.register(dto)
            return ResponseDTO.success_response(new_user)
        except DuplicateEntityError as e:
            return ResponseDTO.error_response(str(e))