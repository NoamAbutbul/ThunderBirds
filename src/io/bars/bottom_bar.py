"""
    File to define the bottombar of the game.
"""


from src.configuration_files import GameInformationColors
from src.io.bars import Bar
from src.io.output import OutputInterface
from src.logger import logger


class BottomBar(Bar):
    """Represent a bottombar.

    Attributes: 
        output_manager (OutputInterface): output manager for the game
        player_msg (str): player message to show
        header (str): header of the game
    """

    GAME_HEADER = "----ThunderBirds----"
    PLAYER_MSG_POSITION = 9
    HEADER_POSITION = 36

    def __init__(self, output_manager: OutputInterface, player_msg: str = "") -> None:
        """Initializes a new instance of the Bar class.

        Args:
            output_manager (OutputInterface): output manager for the game
            player_msg (str, optional): player message to show. Defaults to "".
        """
        super().__init__(output_manager)
        self.__player_msg: str = player_msg
        self.__header: str = BottomBar.GAME_HEADER

    @property
    def player_msg(self) -> str:
        return self.__player_msg

    @player_msg.setter
    def player_msg(self, value: str) -> None:
        self.__player_msg = value

    @property
    def header(self) -> str:
        return self.__header

    @header.setter
    def header(self, value: str) -> None:
        self.__header = value

    def format_bar_to_print(self) -> str:
        """Format the bottombar to print.

        Returns:
            str: the formatted bottombar
        """
        bar_str = f"Player: {self.__player_msg}\t\t\t   "
        bar_str += f"{self.__header}"
        return bar_str

    def show(self) -> None:
        """Show the bottombar. """
        logger.debug(f"Current bottombar: {self.__str__()}")
        self.output_manager.print_bottombar(self.format_bar_to_print())
        self.show_player_message()
        self.show_header(self.output_manager.Color.get_color_by_name(
            GameInformationColors.HEADER.value))

    def clear(self) -> None:
        """Clear the bottombar. """
        self.output_manager.clear_bottombar()

    def show_player_message(self, color: OutputInterface.Color = None) -> None:
        """Show player message.

        Args:
            color (Color, optional): message color. Defaults to None.
        """
        self.output_manager.print_at(
            self.__player_msg, OutputInterface.BOTTOMBAR_POSITION, BottomBar.PLAYER_MSG_POSITION, color)

    def show_header(self, color: OutputInterface.Color = None) -> None:
        """Show header.

        Args:
            color (Color, optional): header color. Defaults to None.
        """
        self.output_manager.print_at(
            self.__header, OutputInterface.BOTTOMBAR_POSITION, BottomBar.HEADER_POSITION, color)

    def delete_player_msg(self) -> None:
        """Delete first message. """
        self.output_manager.delete_msg(
            1, OutputInterface.BOTTOMBAR_POSITION, BottomBar.PLAYER_MSG_POSITION)

    def delete_header(self) -> None:
        """Delete header. """
        self.output_manager.delete_msg(
            BottomBar.MAX_HEADER_LENGTH, OutputInterface.BOTTOMBAR_POSITION, BottomBar.HEADER_POSITION)

    def update_player_msg(self, msg: str, color: OutputInterface.Color = None) -> None:
        """Update player message.

        Args:
            msg (str): new message
            color (Color, optional): message color. Defaults to None.
        """
        self.delete_player_msg()
        self.__player_msg = msg
        self.show_player_message(color)

    def update_header(self, header: str) -> None:
        """Update header message.

        Args:
            header (str): new header
        """
        self.delete_header()
        self.__header = header
        self.show_header(self.output_manager.Color.get_color_by_name(
            GameInformationColors.HEADER.value))

    def __str__(self) -> str:
        """Get bottombar description.

        Returns:
            str: bottombar description
        """
        ret_str = f"Player = {self.__player_msg}, header = {self.__header}"
        return ret_str
