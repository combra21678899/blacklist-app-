class BadRequestError(Exception):
    """Exception raised for bad requests (400)."""
    def __init__(self, message="Bad Request"):
        self.message = message
        super().__init__(self.message)


class NotFoundError(Exception):
    """Exception raised for not found (404)."""
    def __init__(self, message="Not Found"):
        self.message = message
        super().__init__(self.message)


class ConflictError(Exception):
    """Exception raised for conflict (409)."""
    def __init__(self, message="Conflict"):
        self.message = message
        super().__init__(self.message)


class UnauthorizedError(Exception):
    """Exception raised for unauthorized (401)."""
    def __init__(self, message="Unauthorized"):
        self.message = message
        super().__init__(self.message)