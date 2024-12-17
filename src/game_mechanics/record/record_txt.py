"""
    File to define the RecorderTxt of the game.
"""


import glob
import os
import time
from typing import Callable
from src.game_mechanics.record.record_interface import RecordInterface
from src.game_consts import RECORDS_DIR_PATH, RECORD_FILE_EXTENSION, LONG_SLEEP, MAX_RECORDS_FILES
from src.io.input import InputInterface
from src.io.output import OutputInterface
from src.logger import logger


class RecorderTxt(RecordInterface):
    """RecorderTxt to implement RecordInterface with the txt records file. 

    Attributes:
        input_manager (InputInterface): input manager for the game
        output_manager (OutputInterface): output manager for the game
        record_content (str): record file content
        is_start_key (bool): flag to notice is start key
        prev_key (str): key name for previous button pressed
        start_time (float): start time for pressing key
        end_time (float): end time for pressing key
        hook (Callable): hook for record user input
        level_filename (str): filename of the level
        time_for_game (int): time for the game
        hearts_for_game (int): hearts for the game
    """

    TXT_EXTENSION = ".txt"
    START_STRING = "Start"

    def __init__(self, input_manager: InputInterface, output_manager: OutputInterface, level_filename: str, time_for_game: int, hearts_for_game: int) -> None:
        """Initializes a new instance of the RecorderTxt class.

        Args:
            input_manager (InputInterface): input manager for the game
            output_manager (OutputInterface): output manager for the game
            level_filename (str): filename of the level
            time_for_game (int): time for the game
            hearts_for_game (int): hearts for the game
        """
        self.__input_manager: InputInterface = input_manager
        self.__output_manager: OutputInterface = output_manager
        self.__record_content: str = ""
        # TODO -> continue here!!
