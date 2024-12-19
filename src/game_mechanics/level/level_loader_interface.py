"""
    File to define LevelLoaderInterface.
"""


from abc import ABC, abstractmethod


class LevelLoaderInterface(ABC):
    """An interface for loading levels. """

    @abstractmethod
    def load_current_level(self) -> list[list[str]]:
        """Load the current level.

        Returns:
            list[list[str]]: the current level matrix
        """
        raise NotImplementedError

    @abstractmethod
    def load_level_by_name(self, filename: str) -> list[list[str]]:
        """Load a level by its name.

        Args:
            filename (str): the name of the level file

        Returns:
            list[list[str]]: the level matrix
        """
        raise NotImplementedError

    @abstractmethod
    def load_next_level(self) -> list[list[str]]:
        """Load the next level.

        Returns:
            list[list[str]]: the next level matrix
        """
        raise NotImplementedError

    @abstractmethod
    def get_current_level_filename(self) -> str:
        """Get current level filename.

        Returns:
            str: current level filename
        """
        raise NotImplementedError

    @abstractmethod
    def is_next_level_exist(self) -> bool:
        """Check if there is next level.

        Returns:
            bool: True - if next level exist, else False
        """
        raise NotImplementedError
