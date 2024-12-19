"""
    File to define PortalError of the game.
"""


from src.game_pieces.game_objects.game_object_exception import GameObjectError


class PortalError(GameObjectError):
    """Exception class for portal error. """

    def __init__(self, message: str) -> None:
        """Initializes a new instance of the PortalError class.

        Args:
            message (str): message for the exception
        """
        message = f"[Portal]: {message}"
        super().__init__(message)


class PortalSizeError(PortalError):
    """Exception class for portal size error. """

    def __init__(self, message: str) -> None:
        """Initializes a new instance of the PortalSizeError class.

        Args:
            message (str): message for the exception
        """
        message = f"[PortalSize]: {message}"
        super().__init__(message)
