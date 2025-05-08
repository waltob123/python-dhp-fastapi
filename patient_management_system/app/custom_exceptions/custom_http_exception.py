class CustomHTTPException(Exception):
    """
    Custom exception class for HTTP errors.
    """
    def __init__(self, status_code: int, message: str, success: bool = False) -> None:
        self.status_code = status_code
        self.message = message
        self.success = success

    def __str__(self):
        return f"HTTP {self.status_code}: {self.message}"
