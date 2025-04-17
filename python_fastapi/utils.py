import random

from python_fastapi.constants import MINIMUM_PASSWORD_LENGTH


def generate_id() -> int:
    """
    Generate a unique id for the user

    :return: int
    """
    return random.randint(1, 1000000)


def validate_password(password: str) -> str:
    if len(password) < MINIMUM_PASSWORD_LENGTH:
        raise ValueError("Password must be at least 8 characters long")
    if not any(char.isdigit() for char in password):
        raise ValueError("Password must contain at least one digit")
    if not any(char.isalpha() for char in password):
        raise ValueError("Password must contain at least one letter")
    return password


def offset_calculator(page: int, page_size: int) -> int:
    """
    Calculate the offset for pagination

    :param page: The page number
    :param page_size: The number of items per page
    :return: int
    """
    if page < 1 or page_size < 1:
        raise ValueError("Page and page size must be greater than 0")
    return (page - 1) * page_size