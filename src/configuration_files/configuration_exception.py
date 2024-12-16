"""
    File to define ConfigurationError of the game.
"""


from src.exceptions import BasicException


class ConfigurationError(BasicException):
    """Exception class for configuration file loading error. """

    def __init__(self, message: str) -> None:
        """Initializes a new instance of the ConfigurationError class.

        Args:
            message (str): message for the exception
        """
        message = f"[Configuration]: {message}"
        super().__init__(message)


class ColorError(ConfigurationError):
    """Exception class for colors error. """

    def __init__(self, message: str) -> None:
        """Initializes a new instance of the ColorError class.

        Args:
            message (str): message for the exception
        """
        message = f"[Color]: {message}"
        super().__init__(message)


class BoardSizeError(ConfigurationError):
    """Exception class for board size error. """

    def __init__(self, message: str) -> None:
        """Initializes a new instance of the BoardSizeError class.

        Args:
            message (str): message for the exception
        """
        message = f"[BoardSize]: {message}"
        super().__init__(message)
