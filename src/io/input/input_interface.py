"""
    File to define the InputInterface of the game.
"""


from enum import Enum
from abc import ABC, abstractmethod
from typing import Any, Callable


class InputInterface(ABC):
    """Define base input interface to the game. """

    class Buttons(Enum):
        """Enum that represent buttons available in the game. """
        SHIP_SWITCH = ...
        UP = ...
        DOWN = ...
        LEFT = ...
        RIGHT = ...
        ENTER = ...
        EXIT = ...
        UP_ARROW = ...
        DOWN_ARROW = ...

    def __init__(self, source: Any, speed: list[float]) -> None:
        """Initializes a new instance of the InputInterface class.

        Args:
            source (Any): source data
            speed (list[float]): list with one item, speed of the game frame
        """
        super().__init__()
        self.__source: str = source
        self.__speed: list[float] = speed

    @property
    def source(self) -> str:
        return self.__source

    @property
    def speed(self) -> float:
        return self.__speed[0]

    @speed.setter
    def speed(self, value: float) -> None:
        self.__speed[0] = value

    @abstractmethod
    def get_buttons(self) -> Buttons:
        """Get available input buttons.

        Returns:
            Buttons: available input buttons
        """
        return InputInterface.Buttons

    @abstractmethod
    def start_listening(self, callback: Callable) -> Callable:
        """Start listening to input.
            and activate callback when input is valid.

        Args:
            callback (Callable): callback to active with the valid input

        Returns:
            Callable: hook callable
        """
        raise NotImplementedError

    @abstractmethod
    def stop_listening(self, callback: Callable) -> None:
        """Stop listening to input
            deactivate hook by callback.

        Args:
            callback (Callable): callback to deactivate
        """
        raise NotImplementedError
