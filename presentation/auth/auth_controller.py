from presentation.auth.auth_web_service import AuthWebService
from presentation.auth.dtos.authenticated_user_dto import AuthenticatedUserDTO
from presentation.auth.dtos.login_credentials_dto import LoginCredentialsDTO
from presentation.auth.dtos.new_user_dto import NewUserDTO
from presentation.dtos.request_dto import RequestDTO
from presentation.dtos.response_dto import ResponseDTO
from presentation.user.dtos.user_dto import UserDTO
from application.errors.invalid_credentials_error import InvalidCredentialsError
from application.errors.duplicate_entity_error import DuplicateEntityError


class AuthController:
    def __init__(self, web_service: AuthWebService):
        self._web_service = web_service

    def login(self, request: RequestDTO) -> ResponseDTO[AuthenticatedUserDTO]:
        credentials = LoginCredentialsDTO.from_dict(request.body)

        if not credentials:
            return ResponseDTO(success=False, message="Invalid credentials")

        try:
            user = self._web_service.login(credentials)
            return ResponseDTO.success_response(user)
        except InvalidCredentialsError as e:
            return ResponseDTO.error_response(str(e))

    def register(self, request: RequestDTO) -> ResponseDTO[UserDTO]:
        dto = NewUserDTO.from_dict(request.body)

        if not dto:
            return ResponseDTO(success=False, message="There are missing fields! Please, fill each one of them.")

        try:
            new_user = self._web_service.register(dto)
            return ResponseDTO.success_response(new_user)
        except DuplicateEntityError as e:
            return ResponseDTO.error_response(str(e))
