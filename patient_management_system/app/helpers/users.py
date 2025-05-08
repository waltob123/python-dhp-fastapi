def check_email_uniqueness(list_of_users, email):
    """
    Check if the email is unique in the list of users.

    Args:
        list_of_users (list): List of user dictionaries.
        email (str): Email to check.

    Returns:
        bool: True if the email is unique, False otherwise.
    """
    for user in list_of_users:
        if user["email"] == email:
            return False
    return True


def get_users_list():
    """
    Get the list of users.

    Returns:
        list: List of user dictionaries.
    """
    from app.dummy_data import users
    return users
