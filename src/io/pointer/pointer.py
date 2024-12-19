"""
    File to define the Pointer util.
"""


from typing import Callable
from src.io.output import OutputInterface
from src.io.input import InputInterface
from src.game_pieces.symbols import ViewSymbol


class Pointer:
    """Represent a pointer.

    Attributes:
        output_manager (OutputInterface): output manager for the game
        input_manager (InputInterface): input manager for the game
        symbol (str): pointer symbol
        callbacks (list[(int, int, Callable)]): positions and functions list to pointed to
        callback_index (int): function list index
        hook (Callable): hook for input listening
    """

    SPACER_FROM_POINTED = 2

    def __init__(self, output_manager: OutputInterface, input_manager: InputInterface, callbacks: list[(int, int, Callable)]) -> None:
        """Initializes a new instance of the Pointer class.

        Args:
            output_manager (OutputInterface): output manager for the game
            input_manager (InputInterface): input manager for the game
            callbacks (list[): positions and functions list to pointed to
        """
        self.__output_manager: OutputInterface = output_manager
        self.__input_manager: InputInterface = input_manager
        self.__symbol: str = ViewSymbol.POINTER.value
        self.__callbacks: list[(int, int, Callable)] = callbacks
        self.__callback_index: int = 0
        self.__hook: Callable = None

    def click_enter_pointed(self) -> None:
        """Click enter to the pointer.
            this function activate the callback that the pointer pointed to.
        """
        if len(self.__callbacks) > 0:
            callback, args, kwargs = self.__callbacks[self.__callback_index][2]
            callback(*args, **kwargs)

    def click_delete_pointed(self) -> None:
        pass

    def move_down(self) -> None:
        """Move the pointer down. """
        if len(self.__callbacks) > 0:
            self.remove()
            self.__callback_index = (
                self.__callback_index + 1) % len(self.__callbacks)
            self.show()

    def move_up(self) -> None:
        """Move the pointer up. """
        if len(self.__callbacks) > 0:
            self.remove()
            self.__callback_index = (
                self.__callback_index - 1) % len(self.__callbacks)
            self.show()

    def show(self) -> None:
        """Show the pointer. """
        if len(self.__callbacks) > 0:
            row = self.__callbacks[self.__callback_index][0]
            col = self.__callbacks[self.__callback_index][1] - \
                Pointer.SPACER_FROM_POINTED
            self.__output_manager.print_at(
                self.__symbol, row, col, self.__output_manager.Color.GREEN)

    def remove(self) -> None:
        """Remove the pointer from the output. """
        if len(self.__callbacks) > 0:
            row = self.__callbacks[self.__callback_index][0]
            col = self.__callbacks[self.__callback_index][1] - \
                Pointer.SPACER_FROM_POINTED
            self.__output_manager.delete_at(row, col)

    def activate(self) -> None:
        """Activate the pointer
            and listen to user input.
        """
        buttons = self.__input_manager.get_buttons()

        def handle_input(key: str) -> None:
            """Callback to handle user input.

            Args:
                key (str): key from the user input
            """
            actions = {
                buttons.ENTER.value: self.click_enter_pointed,
                buttons.UP.value: self.move_up,
                buttons.DOWN.value: self.move_down
            }
            if key in actions:
                actions[key]()

        self.__hook = self.__input_manager.start_listening(handle_input)

    def deactivate(self) -> None:
        """Deactivate the pointer
            and stop listen to user input.
        """
        if self.__hook is not None:
            self.__input_manager.stop_listening(self.__hook)
        self.__hook = None
