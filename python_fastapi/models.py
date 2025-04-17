from datetime import datetime, timezone

from python_fastapi.mixins import PersistMixin
from python_fastapi.utils import generate_id


class User(PersistMixin):
    def __init__(self, email: str, username: str, password: str, created_at: str = None) -> None:
        """
        Constructor for User class

        :param email: The email of the user
        :param username:  The username of the user
        :param password:  The password of the user
        """
        self.__email = email
        self.__username = username
        self.__password = password
        self.__id = generate_id()
        self.__updated_at = None
        self.__deleted_at = None
        self.__is_active = False

        if created_at is None:
            self.__created_at = datetime.now(timezone.utc)
        else:
            self.__created_at = datetime.strptime(created_at, "%Y-%m-%d %H:%M:%S.%f")

    @property
    def email(self) -> str:
        """
        Getter for email

        :return: The email of the user
        """
        return self.__email

    @property
    def username(self) -> str:
        """
        Getter for username

        :return: The username of the user
        """
        return self.__username

    @property
    def password(self) -> str:
        """
        Getter for password

        :raise: NotImplementedError
        """
        raise NotImplementedError("Password is not accessible")

    @property
    def id(self) -> int:
        """
        Getter for id

        :return: The id of the user
        """
        return self.__id

    @property
    def created_at(self) -> datetime:
        """
        Getter for created_at

        :return: The created_at timestamp of the user
        """
        return self.__created_at

    @property
    def updated_at(self) -> datetime | None:
        """
        Getter for updated_at

        :return: The updated_at timestamp of the user
        """
        return self.__updated_at

    @property
    def deleted_at(self) -> datetime | None:
        """
        Getter for deleted_at

        :return: The deleted_at timestamp of the user
        """
        return self.__deleted_at

    @property
    def is_active(self) -> bool:
        """
        Getter for is_active

        :return: The is_active status of the user
        """
        return self.__is_active

    @email.setter
    def email(self, email: str) -> None:
        """
        Setter for email

        :param email: The email of the user
        """
        self.__email = email

    @username.setter
    def username(self, username: str) -> None:
        """
        Setter for username

        :param username: The username of the user
        """
        self.__username = username

    @password.setter
    def password(self, password: str) -> None:
        """
        Setter for password

        :param password: The password of the user
        """
        self.__password = password

    @updated_at.setter
    def updated_at(self, updated_at: datetime) -> None:
        """
        Setter for updated_at

        :param updated_at: The updated_at timestamp of the user
        """
        self.__updated_at = updated_at

    @deleted_at.setter
    def deleted_at(self, deleted_at: datetime) -> None:
        """
        Setter for deleted_at

        :param deleted_at: The deleted_at timestamp of the user
        """
        self.__deleted_at = deleted_at

    @is_active.setter
    def is_active(self, is_active: bool) -> None:
        """
        Setter for is_active

        :param is_active: The is_active status of the user
        """
        self.__is_active = is_active

    def to_dict(self) -> dict:
        """
        Convert the user object to a dictionary

        :return: A dictionary representation of the user object
        """
        return {
            "id": self.__id,
            "email": self.__email,
            "username": self.__username,
            "password": self.__password,
            "created_at": str(self.__created_at),
            "updated_at": str(self.__updated_at),
            "deleted_at": str(self.__deleted_at),
            "is_active": self.__is_active
        }

    def __str__(self) -> str:
        """
        String representation of the user object

        :return: A string representation of the user object
        """
        return f"<{self.__class__.__name__} {self.email}>"

    def __repr__(self) -> str:
        """
        String representation of the user object

        :return: A string representation of the user object
        """
        return f"{self.__class__.__name__}({self.__email}, {self.__username}, {self.__password})"
