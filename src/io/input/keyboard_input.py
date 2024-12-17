"""
    File to define the KeyboardInput class.
"""


import keyboard
from keyboard._keyboard_event import KeyboardEvent
from enum import Enum
from typing import Any, Callable
from src.configuration_files import KEYBOARD_BUTTONS
from src.io.input.input_interface import InputInterface
from src.logger import logger


class KeyboardInput(InputInterface):
    """Keyboard to implement InputInterface with the keyboard. """

    class Buttons(Enum):
        """Enum that represent buttons available in the game. """
        SHIP_SWITCH = KEYBOARD_BUTTONS['SHIP_SWITCH']
        UP = KEYBOARD_BUTTONS['UP']
        DOWN = KEYBOARD_BUTTONS['DOWN']
        LEFT = KEYBOARD_BUTTONS['LEFT']
        RIGHT = KEYBOARD_BUTTONS['RIGHT']
        ENTER = 'enter'
        EXIT = 'esc'
        UP_ARROW = 'up'
        DOWN_ARROW = 'down'

    def __init__(self, source: Any, speed: list[float]) -> None:
        """Initializes a new instance of the KeyboardInput class. """
        super().__init__("", None)

    def get_buttons(self) -> Buttons:
        """Get available keyboard input buttons.

        Returns:
            Buttons: available input buttons
        """
        return KeyboardInput.Buttons

    def start_listening(self, callback: Callable) -> Callable:
        """Start listening to keyboard input.
            and activate callback when input is valid.

        Args:
            callback (Callable): callback to active with the valid input

        Returns:
            Callable: hook callable
        """
        def validate_key(key_event: KeyboardEvent) -> None:
            """Validate key input.

            Args:
                key_event (KeyboardEvent): key event that triggered
            """
            logger.debug(f"in on_press callback: key = {key_event}")
            buttons_values = [button.value for _,
                              button in KeyboardInput.Buttons.__members__.items()]
            if key_event.name not in buttons_values:
                return
            callback(key_event.name)

        hook_callable = keyboard.on_press(validate_key)
        return hook_callable

    def stop_listening(self, callback: Callable) -> None:
        """Stop listening to input
            deactivate hook by callback.

        Args:
            callback (Callable): callback to deactivate
        """
        if callback is not None:
            keyboard.unhook(callback)
