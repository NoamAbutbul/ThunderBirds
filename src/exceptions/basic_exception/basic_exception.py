"""
    File to define basic game exception.
"""


from src.logger import logger


class BasicException(Exception):
    """Define basic game exception. """

    def __init__(self, message: str) -> None:
        """Initializes a new instance of the BasicException class.

        Args:
            message (str): message for the exception
        """
        logger.error(message)
        super().__init__(message)
        self.__message = message

    def __str__(self) -> str:
        """Get exception description.

        Returns:
            str: exception description
        """
        return self.__message
