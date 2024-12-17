"""
    File to define the FileInput class.
"""


import time
from typing import Any, Callable
from enum import Enum
from src.io.input.input_interface import InputInterface
from src.io.input.keyboard_input import KeyboardInput
from src.logger import logger
from threading import Thread
from src.game_consts import GAME_SPEED, SPEED_STEPS


class FileInput(InputInterface):
    """FileInput to implement InputInterface with file source .record format. """

    class Buttons(Enum):
        """Enum that represent buttons available in the game. """
        SHIP_SWITCH = 'g'
        UP = 'w'
        DOWN = 's'
        LEFT = 'a'
        RIGHT = 'd'
        ENTER = 'enter'
        EXIT = 'esc'
        UP_ARROW = 'up'
        DOWN_ARROW = 'down'

    def __init__(self, source: Any, speed: list[float]) -> None:
        """Initializes a new instance of the FileInput class.

        Args:
            source (Any): source path file
            speed (list[float]): list with one item, speed of the game frame
        """
        super().__init__(source, speed)
        self.__can_stream: bool = False
        self.__raw_speed: float = speed[0]

    def get_buttons(self) -> Buttons:
        """Get available fileinput buttons.

        Returns:
            Buttons: available input buttons
        """
        return FileInput.Buttons

    def start_listening(self, callback: Callable) -> None:
        """Start streaming input file
            and activate callback when input is valid.

        Args:
            callback (Callable): callback to active with the valid input
        """
        self.__can_stream = True

        def input_streaming():
            """Streaming the file source as input game. """
            with open(self.source, 'r') as file:
                lines = file.readlines()

            line_index = 3
            while line_index < len(lines) and self.__can_stream:
                line = lines[line_index]
                line_index += 1

                button = line.split(" ")[0]
                sec = float(line.split(" ")[1])

                self.speed = self.__raw_speed
                callback(button)
                slp_time = (sec * (1/self.speed))
                logger.debug(f"key = {button}, time to sleep = {slp_time}")
                time.sleep(slp_time)

        def speed_control():
            """Add watch speed control listener. """
            keyboard_manager = KeyboardInput("", None)

            def handle_input(key: str) -> None:
                buttons = keyboard_manager.get_buttons()
                actions = {
                    buttons.UP_ARROW.value: self.increase_speed,
                    buttons.DOWN_ARROW.value: self.decrease_speed
                }
                if key == buttons.EXIT.value:
                    callback(key)
                if key in actions:
                    actions[key]()

            keyboard_manager.start_listening(handle_input)

        speed_control_listener = Thread(target=speed_control)
        speed_control_listener.start()
        file_streaming_thread = Thread(target=input_streaming)
        file_streaming_thread.start()

    def increase_speed(self) -> None:
        """Increase game watch speed. """
        if self.__raw_speed < GAME_SPEED["MAX_SPEED"]:
            self.__raw_speed *= SPEED_STEPS

    def decrease_speed(self) -> None:
        """Decrease game watch speed. """
        if self.__raw_speed > GAME_SPEED["MIN_SPEED"]:
            self.__raw_speed /= SPEED_STEPS

    def stop_listening(self, callback: Callable) -> None:
        """Stop streaming input

        Args:
            callback (Callable): callable to deactivate
        """
        self.__can_stream = False
