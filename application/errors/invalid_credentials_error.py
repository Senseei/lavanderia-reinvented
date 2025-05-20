class InvalidCredentialsError(Exception):
    """Exception raised for invalid credentials."""

    def __init__(self, message: str = "Invalid credentials provided."):
        self.message = message
        super().__init__(self.message)