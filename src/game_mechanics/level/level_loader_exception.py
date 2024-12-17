"""
    File to define LevelLoaderError of the game.
"""


from src.exceptions import BasicException


class LevelLoaderError(BasicException):
    """Exception class for level loading errors. """

    def __init__(self, message: str) -> None:
        """Initializes a new instance of the LevelLoaderError class.

        Args:
            message (str): message for the exception
        """
        message = f"[LevelLoader]: {message}"
        super().__init__(message)


class LevelSizeError(LevelLoaderError):
    """Exception class for level size error. """

    def __init__(self, message: str) -> None:
        """Initializes a new instance of the LevelSizeError class.

        Args:
            message (str): message for the exception
        """
        message = f"[LevelSize]: {message}"
        super().__init__(message)


class LevelPathError(LevelLoaderError):
    """Exception class for level path error. """

    def __init__(self, message: str) -> None:
        """Initializes a new instance of the LevelPathError class.

        Args:
            message (str): message for the exception
        """
        message = f"[LevelPath]: {message}"
        super().__init__(message)


class LevelSymbolsError(LevelLoaderError):
    """Exception class for level symbols error. """

    def __init__(self, message: str) -> None:
        """Initializes a new instance of the LevelSymbolsError class.

        Args:
            message (str): message for the exception
        """
        message = f"[LevelSymbols]: {message}"
        super().__init__(message)


class LevelElementsError(LevelLoaderError):
    """Exception class for level elements error. """

    def __init__(self, message: str) -> None:
        """Initializes a new instance of the LevelElementsError class.

        Args:
            message (str): message for the exception
        """
        message = f"[LevelElements]: {message}"
        super().__init__(message)
