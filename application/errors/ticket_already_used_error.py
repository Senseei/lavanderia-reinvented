class TicketAlreadyUsedError(Exception):
    """Exception raised when a ticket has already been used."""

    def __init__(self, message="This ticket has already been used."):
        self.message = message
        super().__init__(self.message)

    def __str__(self):
        return self.message