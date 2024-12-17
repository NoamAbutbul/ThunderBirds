"""
    File to define the OutputInterface of the game.
"""


from abc import ABC, abstractmethod
from src.configuration_files import ROWS, COLS
from enum import Enum


class OutputInterface(ABC):
    """Define base output interface to the game. """

    MENUBAR_POSITION = 1
    BOARD_POSITION = 2
    BOTTOMBAR_POSITION = BOARD_POSITION + ROWS

    class Color(Enum):
        """Enum that represent colors in the game. """
        RED = ...
        GREEN = ...
        YELLOW = ...
        BLUE = ...
        MAGENTA = ...
        CYAN = ...
        WHITE = ...
        GREY = ...
        BLACK = ...
        LIGHT_RED = ...
        LIGHT_GREEN = ...
        LIGHT_YELLOW = ...
        LIGHT_BLUE = ...
        LIGHT_MAGENTA = ...
        LIGHT_CYAN = ...
        RESET = ...

        @abstractmethod
        def get_color_by_name(color_name: str) -> "OutputInterface.Color":
            """Get color object by its name.

            Args:
                color_name (str): color name

            Returns:
                Color: color object matched
            """
            if color_name == "":
                return OutputInterface.Color.RESET
            color = OutputInterface.Color[color_name.upper()]
            return color

    @abstractmethod
    def config(self) -> None:
        """Config the output window settings for the game. """
        raise NotImplementedError

    @abstractmethod
    def set_title(self, title: str) -> None:
        """Set output title.

        Args:
            title (str): title to show
        """
        raise NotImplementedError

    @abstractmethod
    def set_output_size(self, width: int, height: int) -> None:
        """Set the output window size.

        Args:
            width (int): width of the window
            height (int): height of the window
        """
        raise NotImplementedError

    @abstractmethod
    def clear_output(self) -> None:
        """Clear the output window. """
        raise NotImplementedError

    @abstractmethod
    def print_at(self, text: str, x: int, y: int, color: Color = None) -> None:
        """Print at specific position and color to output window.

        Args:
            text (str): text to print
            x (int): x position
            y (int): y position
            color (Color, optional): color for text. Defaults to None.
        """
        raise NotImplementedError

    @abstractmethod
    def delete_at(self, x: int, y: int) -> None:
        """Delete char at position in the output window.

        Args:
            x (int): x position
            y (int): y position
        """
        raise NotImplementedError

    @abstractmethod
    def print_menubar(self, menubar_formatted: str) -> None:
        """Print the menubar to the output window.

        Args:
            menubar_formatted (str): menubar to print
        """
        raise NotImplementedError

    @abstractmethod
    def clear_menubar(self) -> None:
        """Clear the menubar from the output window. """
        raise NotImplementedError

    @abstractmethod
    def print_bottombar(self, bottombar_formatted: str) -> None:
        """Print the bottombar to the output window.

        Args:
            bottombar_formatted (str): bottombar to print
        """
        raise NotImplementedError

    @abstractmethod
    def clear_bottombar(self) -> None:
        """Clear the bottombar from the output window. """
        raise NotImplementedError

    @abstractmethod
    def delete_msg(self, max_msg_len: int, bar_position: int, msg_position: int) -> None:
        """Delete the menubar message from the output window.

        Args:
            max_msg_len (int): maximum length for message
            bar_position (int): bar position
            msg_position (int): message position
        """
        raise NotImplementedError

    @abstractmethod
    def delete_hearts(self, hearts_char_len: int, hearts_position: int) -> None:
        """Delete the menubar hearts from the output window.

        Args:
            hearts_char_len (int): hearts char length
            hearts_position (int): hearts position
        """
        raise NotImplementedError

    @abstractmethod
    def delete_time(self, time_char_len: int, time_position: int) -> None:
        """Delete the menubar time from the output window.

        Args:
            time_char_len (int): time char length
            time_position (int): time position
        """
        raise NotImplementedError

    @abstractmethod
    def print_board(self, board: list[list[str]]) -> None:
        """Print game board to the output window.

        Args:
            board (list[list[str]]): the board to print
        """
        raise NotImplementedError

    @abstractmethod
    def show_text_animation(self, text: str, spacer: int, start_line: int, sleep_time: float, color: Color = None) -> None:
        """Showing text animation to the client.

        Args:
            text (str): text to show
            spacer (int): spacer from the left side
            start_line (int): start line for the animation
            sleep_time (float): sleep time for the animation
            color (Color, optional): color to the text. Defaults to None.
        """
        raise NotImplementedError

    @abstractmethod
    def text_box(self, text: str, line_spacer: int, x: int, y: int, color: Color = None) -> str:
        """Show text box to user and return its input.

        Args:
            text (str): text to print
            line_spacer (int): line spacer to curser inputs
            x (int): x position
            y (int): y position
            color (Color, optional): color for text. Defaults to None.

        Returns:
            str: user input
        """
        raise NotImplementedError
