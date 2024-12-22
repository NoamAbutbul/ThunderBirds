"""
    File to define the menubar of the game.
"""


from src.configuration_files import GameInformationColors
from src.game_pieces import ViewSymbol
from src.io.bars import Bar
from src.io.output import OutputInterface
from src.logger import logger


class MenuBar(Bar):
    """Represent a menubar.

    Attributes: 
        output_manager (OutputInterface): output manager for the game
        msg (str): message to show
        hearts_left (str): hearts left in the game
        time_left (float): time left for the game
    """

    MAX_MSG_LENGTH = 39
    HEARTS_MAX_LENGTH = 6
    MAX_HEARTS = 6
    TIME_MAX_LENGTH = 7
    MSG_POSITION = 0
    HEARTS_POSITION = 66
    TIME_POSITION = 85

    def __init__(self, output_manager: OutputInterface, msg: str = "", hearts_left: int = 0, time_left: float = 0) -> None:
        """Initializes a new instance of the MenuBar class.

        Args:
            output_manager (OutputInterface): output manager for the game
            msg (str, optional): message to show. Defaults to "".
            hearts_left (int, optional): hearts left in the game. Defaults to 0.
            time_left (float, optional): time left for the game. Defaults to 0.
        """
        super().__init__(output_manager)
        if len(msg) > MenuBar.MAX_MSG_LENGTH:
            msg = msg[:MenuBar.MAX_MSG_LENGTH]
        self.__msg: str = msg
        self.__hearts_left: int = min(hearts_left, MenuBar.MAX_HEARTS)
        if len(str(time_left)) > MenuBar.TIME_MAX_LENGTH:
            time_left = float(str(time_left)[:MenuBar.TIME_MAX_LENGTH])
        self.__time_left: float = time_left

    @property
    def msg(self) -> str:
        return self.__msg

    @msg.setter
    def msg(self, value: str) -> None:
        if len(value) > MenuBar.MAX_MSG_LENGTH:
            value = value[:MenuBar.MAX_MSG_LENGTH]
        self.__msg = value

    @property
    def hearts_left(self) -> int:
        return self.__hearts_left

    @hearts_left.setter
    def hearts_left(self, value: int) -> None:
        self.__hearts_left = min(value, MenuBar.MAX_HEARTS)

    @property
    def time_left(self) -> float:
        return self.__time_left

    @time_left.setter
    def time_left(self, value: float) -> None:
        if len(str(value)) > MenuBar.TIME_MAX_LENGTH:
            value = float(str(value)[:MenuBar.TIME_MAX_LENGTH])
        self.__time_left = value

    @property
    def time_char_len(self) -> int:
        return len(str(self.__time_left))

    @property
    def hearts_char_len(self) -> int:
        return self.__hearts_left

    def format_bar_to_print(self):
        """Format the menubar to print.

        Returns:
            str: the formatted menubar
        """
        bar_str = f"{self.__msg}{(MenuBar.MAX_MSG_LENGTH-len(self.__msg))*' '}\t\t\t"  # noqa
        bar_str += f"hearts = {(self.__hearts_left)*ViewSymbol.HEART.value}\ttime left = {self.__time_left}"  # noqa
        return bar_str

    def show(self) -> None:
        """Show the menubar. """
        logger.debug(f"Current menubar: {self.__str__()}")
        self.output_manager.print_menubar(self.format_bar_to_print())
        self.show_msg()
        self.show_hearts(self.output_manager.Color.get_color_by_name(
            GameInformationColors.HEARTS.value))
        self.show_time(self.output_manager.Color.get_color_by_name(
            GameInformationColors.TIME.value))

    def clear(self):
        """Clear the menubar. """
        self.output_manager.clear_menubar()

    def delete_msg(self) -> None:
        """Delete menubar message. """
        self.output_manager.delete_msg(
            MenuBar.MAX_MSG_LENGTH, OutputInterface.MENUBAR_POSITION, MenuBar.MSG_POSITION)

    def delete_hearts(self) -> None:
        """Delete menubar hearts. """
        self.output_manager.delete_hearts(
            self.hearts_char_len, MenuBar.HEARTS_POSITION)

    def delete_time(self) -> None:
        """Delete menubar time. """
        self.output_manager.delete_time(
            self.time_char_len, MenuBar.TIME_POSITION)

    def show_msg(self, color: OutputInterface.Color = None) -> None:
        """Show menubar message.

        Args:
            color (Color, optional): message color. Defaults to None.
        """
        self.output_manager.print_at(
            self.__msg, OutputInterface.MENUBAR_POSITION, MenuBar.MSG_POSITION, color)

    def show_hearts(self, color: OutputInterface.Color = None) -> None:
        """Show menubar hearts.

        Args:
            color (Color, optional): hearts color. Defaults to None.
        """
        self.output_manager.print_at(self.__hearts_left*ViewSymbol.HEART.value,
                                     OutputInterface.MENUBAR_POSITION, MenuBar.HEARTS_POSITION, color)

    def show_time(self, color: OutputInterface.Color = None) -> None:
        """Show menubar time.

        Args:
            color (Color, optional): time color. Defaults to None.
        """
        self.output_manager.print_at(
            self.__time_left, OutputInterface.MENUBAR_POSITION, MenuBar.TIME_POSITION, color)

    def update_msg(self, msg: str) -> None:
        """Update message.

        Args:
            msg (str): new message
        """
        self.delete_msg()
        self.__msg = msg
        self.show_msg()

    def update_hearts(self, hearts: int) -> None:
        """Update hearts.

        Args:
            hearts (int): new hearts
        """
        self.delete_hearts()
        self.__hearts_left = hearts
        self.show_hearts(self.output_manager.Color.get_color_by_name(
            GameInformationColors.HEARTS.value))

    def update_time(self, time: float) -> None:
        """Update time.

        Args:
            time (float): new time
        """
        self.delete_time()
        self.__time_left = time
        self.show_time(self.output_manager.Color.get_color_by_name(
            GameInformationColors.TIME.value))

    def __str__(self):
        """Get menubar description

        Returns:
            _type_: menubar description
        """
        ret_str = f"message = {self.__msg}, hearts_left = {
            self.__hearts_left}, time_left = {self.__time_left}"
        return ret_str
