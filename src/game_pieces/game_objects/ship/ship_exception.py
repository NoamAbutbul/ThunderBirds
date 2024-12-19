"""
    File to define ShipError of the game.
"""


from src.game_pieces.game_objects.game_object_exception import GameObjectError


class ShipError(GameObjectError):
    """Exception class for ship error. """

    def __init__(self, message: str) -> None:
        """Initializes a new instance of the ShipError class.

        Args:
            message (str): message for the exception
        """
        message = f"[Ship]: {message}"
        super().__init__(message)


class ShipSizeError(ShipError):
    """Exception class for ship size error. """

    def __init__(self, message: str) -> None:
        """Initializes a new instance of the ShipSizeError class.

        Args:
            message (str): message for the exception
        """
        message = f"[Size]: {message}"
        super().__init__(message)


class ShipLocationError(ShipError):
    """Exception class for ship location error. """

    def __init__(self, message: str) -> None:
        """Initializes a new instance of the ShipLocationError class.

        Args:
            message (str): message for the exception
        """
        message = f"[Location]: {message}"
        super().__init__(message)
