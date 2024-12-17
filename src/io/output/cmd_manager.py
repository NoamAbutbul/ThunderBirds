"""
    File to define the CMDManager class.
"""


from art import text2art
import msvcrt
import os
import time
from enum import Enum
from typing import Union
from src.io.output.output_interface import OutputInterface
from src.game_pieces import ViewSymbol, LogicSymbol
from src.configuration_files import ROWS, COLS
from src.game_consts import GAME_NAME


class CMDManager(OutputInterface):
    """CMDManager to implement OutputInterface with the Windows CMD. """

    class Color(Enum):
        """Enum that represent colors in the game. """
        RED = "\033[31m"
        GREEN = "\033[32m"
        YELLOW = "\033[33m"
        BLUE = "\033[34m"
        MAGENTA = "\033[35m"
        CYAN = "\033[36m"
        WHITE = "\033[37m"
        GREY = "\033[90m"
        BLACK = "\033[97m"
        LIGHT_RED = "\033[91m"
        LIGHT_GREEN = "\033[92m"
        LIGHT_YELLOW = "\033[93m"
        LIGHT_BLUE = "\033[94m"
        LIGHT_MAGENTA = "\033[95m"
        LIGHT_CYAN = "\033[96m"
        RESET = "\033[0m"

        def get_color_by_name(color_name: str) -> "CMDManager.Color":
            """Get color object by its name.

            Args:
                color_name (str): color name

            Returns:
                Color: color object matched
            """
            if color_name == "":
                return CMDManager.Color.RESET
            color = CMDManager.Color[color_name.upper()]
            return color

    def __init__(self) -> None:
        """Initializes a new instance of the CMDManager class. """
        super().__init__()
        self.__last_position = (0, 0)
        self.__end_position = (ROWS, COLS)

    def config(self) -> None:
        """Config the CMD settings for the game. """
        self.set_title(GAME_NAME)
        self.set_output_size(COLS+1, ROWS+6)
        self.hide_curse()

    def set_title(self, title: str) -> None:
        """Set CMD title.

        Args:
            title (str): title to show
        """
        os.system(f"title {title}")

    def set_output_size(self, width: int, height: int) -> None:
        """Set the CMD window size.

        Args:
            width (int): width of the window
            height (int): height of the window
        """
        os.system(f"mode con: cols={width} lines={height}")

    def hide_curse(self) -> None:
        """Hide the curse for the CMD. """
        print("\033[?25l", end="")

    def clear_output(self) -> None:
        """Clear the CMD. """
        os.system("cls" if os.name == "nt" else "clear")

    def print_at(self, text: str, x: int, y: int, color: Color = None) -> None:
        """Print at specific position and color to CMD.

        Args:
            text (str): text to print
            x (int): x position
            y (int): y position
            color (Color, optional): color for text. Defaults to None.
        """
        self.__last_position = (x, y)
        color_code = CMDManager.Color.RESET.value
        if color is not None:
            color_code = color.value
        print(f"\033[{x};{y}H{color_code}{text}{CMDManager.Color.RESET.value}")
        self.return_to_end_position()

    def delete_at(self, x: int, y: int) -> None:
        """Delete char at position in the CMD.

        Args:
            x (int): x position
            y (int): y position
        """
        print(f"\033[{x};{y}H ")
        self.return_to_last_position()

    def print_menubar(self, menubar_formatted: str) -> None:
        """Print the menubar in MENUBAR_POSITION in the CMD.

        Args:
            menubar_formatted (str): menubar to print
        """
        self.print_at(menubar_formatted, CMDManager.MENUBAR_POSITION, 1)

    def clear_menubar(self) -> None:
        """Clear the menubar from the CMD. """
        for col in range(COLS):
            self.delete_at(x=CMDManager.MENUBAR_POSITION, y=col)

    def print_bottombar(self, bottombar_formatted: str) -> None:
        """Print the bottombar to the CMD.

        Args:
            bottombar_formatted (str): bottombar to print
        """
        self.print_at(bottombar_formatted, CMDManager.BOTTOMBAR_POSITION, 1)

    def clear_bottombar(self) -> None:
        """Clear the bottombar from the CMD. """
        for col in range(COLS):
            self.delete_at(x=CMDManager.BOTTOMBAR_POSITION, y=col)

    def delete_msg(self, max_msg_len: int, bar_position: int, msg_position: int) -> None:
        """Delete the menubar message from the CMD.

        Args:
            max_msg_len (int): maximum length for message
            bar_position (int): bar position
            msg_position (int): message position
        """
        for char in range(max_msg_len):
            self.delete_at(x=bar_position, y=char+msg_position)

    def delete_hearts(self, hearts_char_len: int, hearts_position: int) -> None:
        """Delete the menubar hearts from the CMD.

        Args:
            hearts_char_len (int): hearts char length
            hearts_position (int): hearts position
        """
        for char in range(hearts_char_len):
            self.delete_at(x=CMDManager.MENUBAR_POSITION,
                           y=char+hearts_position)

    def delete_time(self, time_char_len: int, time_position: int) -> None:
        """Delete the menubar time from the CMD.

        Args:
            time_char_len (int): time char length
            time_position (int): time position
        """
        for char in range(time_char_len):
            self.delete_at(x=CMDManager.MENUBAR_POSITION, y=char+time_position)

    def prepare_board_to_print(self, board: list[list[str]]) -> list[list[Union[ViewSymbol, str]]]:
        """Gets a logic board (matrix char) and prepare it to show for the client.

        Args:
            board (list[list[str]]): logic board

        Returns:
            list[list[Union[ViewSymbol, str]]]: printable board to the client
        """
        board_to_print = [[None] * COLS for _ in range(ROWS)]
        for row in range(ROWS):
            for col in range(COLS):
                current_element = board[row][col]
                if current_element == LogicSymbol.WALL.value:
                    if (col == 0) or (col == COLS - 1):
                        board_to_print[row][col] = ViewSymbol.WALL_VERTICAL.value
                    elif (row == 0):
                        board_to_print[row][col] = ViewSymbol.WALL_HORIZONTAL_UP.value
                    elif (row == ROWS - 1):
                        board_to_print[row][col] = ViewSymbol.WALL_HORIZONTAL_DOWN.value
                    else:
                        board_to_print[row][col] = ViewSymbol.WALL_VERTICAL.value
                else:
                    view_symbol = ViewSymbol.get_value_by_logic_sign(
                        current_element)
                    board_to_print[row][col] = view_symbol
        return board_to_print

    def print_board(self, board: list[list[str]]) -> None:
        """Print game board to the CMD.

        Args:
            board (list[list[str]]): the board to print
       """
        board = self.prepare_board_to_print(board)
        for row in range(ROWS):
            for col in range(COLS):
                element = board[row][col]
                element_color = ViewSymbol.get_color_by_sign(element)
                x = row + CMDManager.BOARD_POSITION
                y = col + CMDManager.BOARD_POSITION
                self.print_at(
                    element, x, y, CMDManager.Color.get_color_by_name(element_color))
        self.__end_position = (ROWS, COLS)

    def return_to_last_position(self) -> None:
        """Return the curse to the last position saved. """
        x, y = self.__last_position
        print(f"\033[{x};{y}H")

    def return_to_end_position(self) -> None:
        """Return the curse to the end position saved. """
        x, y = self.__end_position
        print(f"\033[{x};{y}H")

    def show_text_animation(self, text: str, spacer: int, start_line: int, sleep_time: float, color: Color = None) -> None:
        """Showing text animation to the client in the CMD.

        Args:
            text (str): text to show
            spacer (int): spacer from the left side
            start_line (int): start line for the animation
            sleep_time (float): sleep time for the animation
            color (Color, optional): color to the text. Defaults to None.
        """
        art_text = text2art(text)
        for line in art_text.splitlines():
            line = (' ' * spacer) + line
            time.sleep(sleep_time)
            self.print_at(line, start_line, 0, color)
            start_line += 1

    def text_box(self, text: str, line_spacer: int, x: int, y: int, color: Color = None) -> str:
        """Show text box to user in the CMD and return its input.

        Args:
            text (str): text to print
            line_spacer (int): line spacer to curser inputs
            x (int): x position
            y (int): y position
            color (Color, optional): color for text. Defaults to None.

        Returns:
            str: user input
        """
        while msvcrt.kbhit():
            msvcrt.getch()
        self.print_at(text + ":", x, y, color)
        user_input = input(f"\033[{x+line_spacer};{y}H")
        return user_input
