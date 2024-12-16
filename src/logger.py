"""
    File to config logger to the game.
"""


import logging
import atexit
from typing import Any


LOG_FILE_PATH = "game_log.log"


class GameLogger(logging.Logger):
    """Extends logging.Logger class to make a custom logger. """

    def __init__(self, name: str, level: int = logging.NOTSET) -> None:
        """Initializes a new instance of the GameLogger class.

        Args:
            name (str): name to logger
            level (int, optional): level to logger. Defaults to logging.NOTSET.
        """
        super().__init__(name, level)

    def log_board(self, msg: str, board: list[list[str]]) -> None:
        """Logging message and board at debug level.

        Args:
            msg (str): message to log before the board
            board (list[list[str]]): board to log
        """
        board_str = ""
        for row in range(len(board)):
            for col in range(len(board[row])):
                board_str += board[row][col]
            board_str += "\n"
        self.debug(f"{msg}:\n{board_str}")

    def log_list(self, msg: str, lst: list[Any]) -> None:
        """Logging message and list at debug level.

        Args:
            msg (str): message to log before the list
            lst (list[Any]): list to log
        """
        header = f" {msg} ".center(70, "-").upper()
        separator = 40 * '-'
        list_str = ""
        for item in lst:
            list_str += f"{item}"
            list_str += f"{separator}"
        self.debug(f"{22 * '-'}>\n{header}{list_str}")

    def clear(self) -> None:
        """Clear all log file. """
        with open(LOG_FILE_PATH, 'w'):
            pass


logger = GameLogger(__name__)
f_handler = logging.FileHandler(LOG_FILE_PATH)
f_format = logging.Formatter('%(asctime)s - %(module)s - %(levelname)s - %(message)s')  # noqa
f_handler.setFormatter(f_format)
logger.addHandler(f_handler)
logger.setLevel(logging.INFO)


def exit_handler() -> None:
    """Define what run at the exit of the program. """
    f_format = logging.Formatter('%(message)s')
    f_handler.setFormatter(f_format)
    logger.addHandler(f_handler)
    logger.info("-" * 80)


atexit.register(exit_handler)
