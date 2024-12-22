"""
    File to define the basic Bar of the game.
"""


from abc import ABC, abstractmethod
from src.io.output import OutputInterface


class Bar(ABC):
    """Represent an abstract bar.

    Attributes: 
        output_manager (OutputInterface): output manager for the game
    """

    def __init__(self, output_manager: OutputInterface) -> None:
        """Initializes a new instance of the Bar class.

        Args:
            output_manager (OutputInterface): output manager for the game
        """
        self.__output_manager: OutputInterface = output_manager

    @property
    def output_manager(self) -> OutputInterface:
        return self.__output_manager

    @abstractmethod
    def format_bar_to_print(self) -> str:
        """Format the bar to print.

        Returns:
            str: the formatted bar
        """
        raise NotImplementedError

    @abstractmethod
    def show(self) -> None:
        """Show the bar. """
        raise NotImplementedError

    @abstractmethod
    def clear(self) -> None:
        """Clear the bar. """
        raise NotImplementedError
