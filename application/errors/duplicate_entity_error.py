class DuplicateEntityError(Exception):
    """Exception raised for duplicate entity errors.

    Args:
        entity (str): The name of the entity that caused the error.
        message (str): A custom error message.
    """

    def __init__(self, entity: str, message: str = "Duplicate entity found."):
        self.entity = entity
        self.message = message
        super().__init__(self.message)