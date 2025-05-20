from adapters.user.dtos.login_credentials_dto import LoginCredentialsDTO
from adapters.user.dtos.response_dto import ResponseDTO
from application.auth.dtos.authenticated_user_dto import AuthenticatedUserDTO
from application.auth.dtos.new_user_dto import NewUserDTO
from application.auth.dtos.user_dto import UserDTO
from application.errors.duplicate_entity_error import DuplicateEntityError
from application.errors.entity_not_found_error import EntityNotFoundError
from application.auth.use_cases.auth_service import AuthService


class AuthControllerAdapter:
    def __init__(self, auth_service: AuthService):
        self._auth_service = auth_service

    def login(self, credentials_dict) -> ResponseDTO[AuthenticatedUserDTO]:
        credentials = LoginCredentialsDTO.from_dict(credentials_dict)

        if not credentials:
            return ResponseDTO(success=False, message="Invalid credentials")

        try:
            user = self._auth_service.login(credentials.username, credentials.password)
            return ResponseDTO.success_response(user)
        except EntityNotFoundError as e:
            return ResponseDTO.error_response(str(e))

    def register(self, user_dict) -> ResponseDTO[UserDTO]:
        dto = NewUserDTO.from_dict(user_dict)

        if not dto:
            return ResponseDTO(success=False, message="There are missing fields! Please, fill each one of them.")

        try:
            new_user = self._auth_service.register(dto)
            return ResponseDTO.success_response(new_user)
        except DuplicateEntityError as e:
            return ResponseDTO.error_response(str(e))