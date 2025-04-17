def check_email_uniqueness(email: str, list_of_users: list[dict]) -> bool:
    """
    Check if email is unique

    :param email: str
    :param list_of_users: list[dict]
    :return: bool
    """
    for user in list_of_users:
        if user.get("email") == email:
            return False
    return True


def get_user_from_list(user_id: int, users_list: list[dict]) -> dict | None:
    """
    Get user from list of users

    :param user_id: the id of the user to get
    :param users_list: the list of users to search from
    :return: dict
    """
    for user in users_list:
        if user.get("id") == user_id:
            return user
    return None
