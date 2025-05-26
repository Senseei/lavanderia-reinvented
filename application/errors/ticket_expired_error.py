class TicketExpiredError(Exception):
    """Exception raised when a ticket has expired."""

    def __init__(self, message="The ticket has expired."):
        self.message = message
        super().__init__(self.message)

    def __str__(self):
        return self.message