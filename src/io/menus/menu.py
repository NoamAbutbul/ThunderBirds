"""
    File to define the basic menu for the game.
"""


from abc import ABC, abstractmethod
from typing import Callable
from src.io.output.output_interface import OutputInterface
from src.io.input.input_interface import InputInterface
from src.game_mechanics.status import Status


class Menu(ABC):
    """Represent a abstract menu.

    Attributes:
        output_manager (OutputInterface): output manager for the game
        input_manager (InputInterface): input manager for the game
        hook (Callable): hook callable for the input handling
        status (Status): status of the game
    """

    def __init__(self, output_manager: OutputInterface, input_manager: InputInterface) -> None:
        """Initializes a new instance of the Menu class.

        Args:
            output_manager (OutputInterface): output manager for the game
            input_manager (InputInterface): input manager for the game
        """
        self.__output_manager: OutputInterface = output_manager
        self.__input_manager: InputInterface = input_manager
        self.__hook: Callable = None
        self.__status: Status = Status.NULL

    @property
    def output_manager(self) -> OutputInterface:
        return self.__output_manager

    @property
    def input_manager(self) -> InputInterface:
        return self.__input_manager

    @property
    def hook(self) -> Callable:
        return self.__hook

    @hook.setter
    def hook(self, value: Callable) -> None:
        self.__hook = value

    @property
    def status(self) -> Status:
        return self.__status

    @status.setter
    def status(self, value: Status) -> None:
        self.__status = value

    @abstractmethod
    def show(self) -> None:
        """Show the menu to the client. """
        raise NotImplementedError

    @abstractmethod
    def activate(self) -> Status:
        """Activate the menu.
            start listen to user input and handle it.

        Returns:
            Status: status for user input
        """
        raise NotImplementedError

    @abstractmethod
    def deactivate(self) -> None:
        """Deactivate the menu.
            release all resources.
        """
        raise NotImplementedError
