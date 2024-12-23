"""
    File that define the Controller of the game.
"""


import sys
import time
from src.game_mechanics import cannot_run_game
from src.exceptions import BasicException
try:
    from src.io import IOManager
except BasicException as e:
    cannot_run_game(e)
from src.game_mechanics.game_mode import GameMode
from src.game_mechanics.game import Game
from src.game_mechanics.status import Status
from src.game_consts import HEARTS, TIME, SHORT_SLEEP
from src.logger import logger


class Controller:
    """Represent the controller of the game.

    Attributes:
        io_manager (IOManager): manager for the IO in the game
        game (Game): manager for the game
        record_name (str): record name of the game
    """

    def __init__(self, io_manager: IOManager = None, game: Game = None) -> None:
        """Initializes a new instance of the Controller class. 

        Args:
            io_manager (IOManager, optional): manager of the IO. Defaults to None.
            game (Game, optional): manager of the game. Defaults to None.
        """
        if isinstance(io_manager, IOManager):
            self.__io_manager: IOManager = io_manager
        else:
            self.__io_manager = IOManager()
        if isinstance(game, Game):
            self.__game: Game = game
        else:
            self.__game = Game(self.__io_manager)
        self.__record_name: str = ""

    def config(self) -> None:
        """Config settings for the game. """
        self.__io_manager.config()

    def run_game(self) -> None:
        """Run the game with all dependencies. """
        try:
            self.config()
            self.activate_start_menu()
        except BasicException as e:
            self.__io_manager.show_exception(e)

    def activate_start_menu(self) -> None:
        """Activate start menu
            and map functions by user input status.
        """
        self.__io_manager.config()
        status = self.__io_manager.activate_start_menu()
        status_action = {
            Status.NEW_GAME: self.start_new_game,
            Status.RULES: self.activate_rules_menu,
            Status.RECORDS: self.activate_records_menu,
            Status.EXIT: self.exit_game
        }
        if status in status_action:
            status_action[status]()

    def activate_rules_menu(self) -> None:
        """Activate rules menu
            and map functions by user input status.
        """
        status = self.__io_manager.activate_rules_menu()
        status_action = {
            Status.EXIT: self.activate_start_menu
        }
        if status in status_action:
            status_action[status]()

    def activate_records_menu(self) -> None:
        """Activate records menu
            and map functions by user input status.
        """
        status, record_name = self.__io_manager.activate_records_menu()
        if record_name != "":
            self.__record_name = record_name
        status_action = {
            Status.EXIT: self.activate_start_menu,
            Status.PLAY_RECORD: self.watch_game
        }
        if status in status_action:
            status_action[status]()

    def start_new_game(self) -> None:
        """Start new game. """
        time.sleep(SHORT_SLEEP)
        logger.info("Starting new game...")
        self.__game = Game(self.__io_manager)
        self.__game.init_new_game(GameMode.PLAY, TIME, HEARTS)
        self.__game.load_level()
        self.__game.start()
        self.activate_start_menu()

    def watch_game(self) -> None:
        """Watch record game. """
        logger.info(f"The record filename is {self.__record_name}")

        def get_record_file_data(record_file: str) -> tuple[str, int, int]:
            """Get record file first data to init game.
                Get level filename, time for game, hearts for game values.

            Args:
                record_file (str): record file path

            Returns:
                tuple[str, int, int]: level_filename, time_for_game, hearts_for_game
            """
            with open(record_file, 'r') as file:
                lines = file.readlines()
            level_filename = lines[0].strip()
            time_for_game = int(lines[1].strip())
            hearts_for_game = int(lines[2].strip())
            return level_filename, time_for_game, hearts_for_game

        level_filename, time_for_game, hearts_for_game = get_record_file_data(
            self.__record_name)
        self.__game.init_new_game(
            GameMode.WATCH, time_for_game, hearts_for_game, self.__record_name)
        self.__game.load_level(level_filename)
        self.__game.start()
        self.activate_start_menu()

    def exit_game(self) -> None:
        """Exit the game. """
        time.sleep(SHORT_SLEEP)
        self.__io_manager.show_goodbye_message()
        logger.info("Exit game...")
        sys.exit()
