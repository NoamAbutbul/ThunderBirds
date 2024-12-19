"""
    File to define GameObjectError of the game.
"""


from src.game_mechanics.level.level_loader_exception import LevelLoaderError


class GameObjectError(LevelLoaderError):
    """Exception class for game object error. """

    def __init__(self, message: str) -> None:
        """Initializes a new instance of the GameObjectError class.

        Args:
            message (str): message for the exception
        """
        message = f"[GameObject]: {message}"
        super().__init__(message)
