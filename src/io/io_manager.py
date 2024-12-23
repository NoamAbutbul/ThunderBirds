"""
    File to define the IOManager class.
"""


import time
from typing import Any, Callable
from src import deps
from src.game_mechanics.game_mode import GameMode
from src.game_mechanics.status import Status
from src.io.input import InputInterface
from src.io.output import OutputInterface
from src.io.menus import Menu, StartMenu, PauseMenu, RulesMenu, RecordMenu
from src.io.bars import MenuBar, BottomBar
from src.io.exceptions import ExceptionView
from src.logger import logger
from src.game_pieces import ViewSymbol, Point


class IOManager:
    """Class to manage all IO in the game.

    Attributes:
        output_manager (OutputInterface): output manager for the game
        input_manager (InputInterface): input manager for the game
        start_menu (Menu): start menu of the game
        menubar (MenuBar): menubar of the game
        bottombar (BottomBar): bottombar of the game
        pause_menu (Menu): pause menu of the game
        rules_menu (Menu): rules menu of the game
        record_menu (Menu): record menu of the game
    """

    def __init__(self) -> None:
        """Initializes a new instance of the IOManager class. """
        self.__output_manager: OutputInterface = deps.get_output_manager()
        self.__input_manager: InputInterface = deps.get_input_manager(
            GameMode.PLAY, "", None)
        self.__start_menu: Menu = StartMenu(
            self.__output_manager, self.__input_manager)
        self.__menubar: MenuBar = MenuBar(self.__output_manager)
        self.__bottombar: BottomBar = BottomBar(self.__output_manager)
        self.__pause_menu: Menu = PauseMenu(
            self.__output_manager, self.__input_manager)
        self.__rules_menu: Menu = RulesMenu(
            self.__output_manager, self.__input_manager)
        self.__record_menu: Menu = RecordMenu(
            self.__output_manager, self.__input_manager)

    @property
    def output_manager(self) -> OutputInterface:
        return self.__output_manager

    @property
    def input_manager(self) -> InputInterface:
        return self.__input_manager

    def set_mode(self, mode: GameMode, source: Any = None, speed: list[float] = None) -> None:
        """Set game mode to make InputInterface as well.

        Args:
            mode (GameMode): mode for the game
            source (Any, optional): source for the InputInterface. Defaults to None.
            speed (list[float], optional): list with one item, speed of the game frame
        """
        self.__input_manager = deps.get_input_manager(mode, source, speed)

    def config(self) -> None:
        """Config settings for the IO. """
        logger.info("Configuring IOManager...")
        self.output_manager.config()

    def get_buttons(self) -> InputInterface.Buttons:
        """Get all input buttons from the input manager.

        Returns:
            InputInterface.Buttons: all input buttons
        """
        return self.input_manager.get_buttons()

    def activate_start_menu(self) -> Status:
        """Activate the start menu.

        Returns:
            Status: status for user input
        """
        logger.info("Activate start menu...")
        status = self.__start_menu.activate()
        return status

    def activate_pause_menu(self) -> Status:
        """Activate the pause menu

        Returns:
            Status: status for user input
        """
        logger.info("Activate pause menu...")
        status = self.__pause_menu.activate()
        return status

    def activate_rules_menu(self) -> Status:
        """Activate the rules menu

        Returns:
            Status: status for user input
        """
        logger.info("Activate rules menu...")
        status = self.__rules_menu.activate()
        return status

    def activate_records_menu(self) -> tuple[Status, str]:
        """Activate the records menu.

        Returns:
            tuple[Status, str]: status for the user input 
                                & record name if need to play record
        """
        logger.info("Activate records menu...")
        status = self.__record_menu.activate()
        record_name = ""
        if status == Status.PLAY_RECORD:
            record_name = self.__record_menu.current_record_file
        return status, record_name

    def print_board(self, board: list[list[str]]) -> None:
        """Print game board to the output.

        Args:
            board (list[list[str]]): the board to print
        """
        self.output_manager.print_board(board)

    def clear_output(self) -> None:
        """Clear the output. """
        self.output_manager.clear_output()

    def show_menubar(self) -> None:
        """Show the menubar to the client. """
        self.__menubar.show()

    def clear_menubar(self) -> None:
        """Clear the menubar. """
        self.__menubar.clear()

    def show_bottombar(self) -> None:
        """Show the bottombar to the client. """
        self.__bottombar.show()

    def clear_bottombar(self) -> None:
        """Clear the bottombar. """
        self.__bottombar.clear()

    def update_menubar_msg(self, msg: str) -> None:
        """Update menubar message.

        Args:
            msg (str): new message
        """
        self.__menubar.update_msg(msg)

    def update_menubar_hearts(self, hearts: int) -> None:
        """Update menubar hearts.

        Args:
            hearts (int): new hearts
        """
        self.__menubar.update_hearts(hearts)

    def update_menubar_time(self, new_time: float) -> float:
        """Update menubar time.

        Args:
            new_time (float): new time

        Returns:
            float: seconds of the actions
        """
        start_time = time.time()
        self.__menubar.update_time()
        end_time = time.time()
        return end_time - start_time

    def update_bottombar_player_msg(self, msg: str, color: OutputInterface.Color = None) -> None:
        """Update bottombar player message.

        Args:
            msg (str): new message
            color (Color, optional): message color. Defaults to None.
        """
        self.__bottombar.update_player_msg(msg, color)

    def update_bottombar_header(self, msg: str) -> None:
        """Update bottombar header message.

        Args:
            msg (str): new message
        """
        self.__bottombar.update_header(msg)

    def start_listening(self, handle_function: Callable) -> Callable:
        """Listening to the user input.

        Args:
            handle_function (Callable): handle function to activate in any input

        Returns:
            Callable: hook callable
        """
        return self.input_manager.start_listening(handle_function)

    def stop_listening(self, hook: Callable) -> None:
        """Stop listening to the user input.

        Args:
            hook (Callable): hook function to deactivate
        """
        self.input_manager.stop_listening(hook)

    def move_item(self, symbol: str, source: list[Point], dest: list[Point]) -> None:
        """Move an item on the output board.

        Args:
            symbol (str): symbol of the item
            source (list[Point]): source location
            dest (list[Point]): destination location
        """
        view_symbol = ViewSymbol.get_value_by_logic_sign(symbol)
        symbol_color = self.output_manager.Color.get_color_by_name(
            ViewSymbol.get_color_by_sign(view_symbol))
        source_set = set(source)
        dest_set = set(dest)
        source_diff = source_set.difference(dest_set)
        dest_diff = dest_set.difference(source_set)
        for point in source_diff:
            self.output_manager.delete_at(
                point.x+OutputInterface.BOARD_POSITION, point.y+OutputInterface.BOARD_POSITION)
        for point in dest_diff:
            self.output_manager.print_at(
                view_symbol, point.x+OutputInterface.BOARD_POSITION, point.y+OutputInterface.BOARD_POSITION, symbol_color)

    def set_current_player(self, player_symbol: str) -> None:
        """Set current player to output.

        Args:
            player_symbol (str): current player symbol
        """
        view_symbol = ViewSymbol.get_value_by_logic_sign(player_symbol)
        symbol_color = self.output_manager.Color.get_color_by_name(
            ViewSymbol.get_color_by_sign(view_symbol))
        self.update_bottombar_player_msg(view_symbol, symbol_color)

    def time_over(self) -> None:
        """Time over for the game. """
        self.update_menubar_time(0)

    def show_goodbye_message(self) -> None:
        """Showing goodbye message for the client. """
        self.output_manager.clear_output()
        self.output_manager.show_text_animation(
            "GoodBye!!!", 18, 15, 0.05, self.output_manager.Color.GREEN)

    def show_victory_message(self) -> None:
        """Showing victory message for the client. """
        time.sleep(0.3)
        self.output_manager.clear_output()
        self.output_manager.show_text_animation(
            "Game Over", 18, 10, 0.1, self.output_manager.Color.GREEN)
        self.output_manager.show_text_animation(
            "You Won!!!", 18, 17, 0.1, self.output_manager.Color.GREEN)

    def show_lose_message(self) -> None:
        """Showing victory message for the client. """
        time.sleep(0.3)
        self.output_manager.clear_output()
        self.output_manager.show_text_animation(
            "Game Over", 18, 10, 0.1, self.output_manager.Color.RED)
        self.output_manager.show_text_animation(
            "You Lose!!!", 18, 17, 0.1, self.output_manager.Color.RED)

    def show_reduce_life_message(self) -> None:
        """Showing lose message for the client. """
        time.sleep(0.3)
        self.output_manager.clear_output()
        self.output_manager.show_text_animation(
            "Life Reduced", 12, 15, 0.07, self.output_manager.Color.RED)

    def show_exception(self, message: str) -> None:
        """Showing exception to client.

        Args:
            message (str): exception information
        """
        exception_view = ExceptionView(self.output_manager, message)
        exception_view.show()
