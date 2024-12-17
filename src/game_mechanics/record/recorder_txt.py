"""
    File to define the RecorderTxt of the game.
"""


import glob
import os
import time
from typing import Callable
from src.game_mechanics.record.recorder_interface import RecorderInterface
from src.game_consts import RECORDS_DIR_PATH, RECORD_FILE_EXTENSION, LONG_SLEEP, MAX_RECORDS_FILES
from src.io.input import InputInterface
from src.io.output import OutputInterface
from src.logger import logger


class RecorderTxt(RecorderInterface):
    """RecorderTxt to implement RecorderInterface with the txt records file. 

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
        self.__is_start_key: bool = True
        self.__prev_key: str = ""
        self.__start_time: float = 0
        self.__end_time: float = 0
        self.__hook: Callable = None
        self.__level_filename: str = level_filename
        self.__time_for_game: str = time_for_game
        self.__hearts_for_game: str = hearts_for_game
        self.reset_record_file()

    def start_record(self) -> None:
        """Start recording the game. """

        def record_key(key: str) -> None:
            """Record the key pressed.

            Args:
                key (str): The key pressed
            """
            buttons = self.__input_manager.get_buttons()
            keys_to_record = {
                buttons.RIGHT.value,
                buttons.LEFT.value,
                buttons.UP.value,
                buttons.DOWN.value,
                buttons.SHIP_SWITCH.value,
            }
            if (key in keys_to_record) is False:
                return

            if (key == self.__prev_key) and (key != buttons.SHIP_SWITCH.value):
                return

            self.save_prev_key_to_record()
            if self.__is_start_key is True:
                started_time = self.__end_time - self.__start_time
                started_time = round(started_time, 6)
                self.__record_content += f"{RecorderTxt.START_STRING} {str(started_time)}\n"  # noqa

            self.__is_start_key = False
            self.__prev_key = key
            self.__start_time = time.time()

        self.__start_time: float = time.time()
        self.__hook = self.__input_manager.start_listening(record_key)

    def stop_record(self) -> None:
        """Stop recording the game. """
        if self.__hook is not None:
            self.__input_manager.stop_listening(self.__hook)
        self.__hook = None

    def save_prev_key_to_record(self) -> None:
        """Save the previous key to the record file. """
        self.__end_time = time.time()
        time_pressed = self.__end_time - self.__start_time
        time_pressed = round(time_pressed, 6)
        if (not self.__is_start_key):
            self.__record_content += f"{self.__prev_key} {str(time_pressed)}\n"

    def save_record(self) -> None:
        """Save the record to new file by user input. """
        self.save_prev_key_to_record()
        self.__output_manager.clear_output()
        self.__output_manager.print_at(
            "If you don't want to save press Enter", 16, 30, self.__output_manager.Color.YELLOW)
        filename = self.__output_manager.text_box(
            "Enter filename for the save record file", 2, 15, 30, self.__output_manager.Color.YELLOW)
        if filename == "":
            return

        self.enforce_max_records_files()
        file_path = os.path.join(
            RECORDS_DIR_PATH, filename + RECORD_FILE_EXTENSION + RecorderTxt.TXT_EXTENSION)
        self.write_record_to_file(file_path)
        self.__output_manager.print_at(
            "File saved successfully", 25, 35, self.__output_manager.Color.GREEN)
        time.sleep(LONG_SLEEP)
        self.__output_manager.clear_output()
        self.reset_record_file()

    def enforce_max_records_files(self) -> None:
        """Enforce there is amount record files under maximum value.
            Remove oldest records if there is too much.
        """
        records_files = glob.glob(
            RECORDS_DIR_PATH + '/*' + RECORD_FILE_EXTENSION + RecorderTxt.TXT_EXTENSION)
        while len(records_files) >= MAX_RECORDS_FILES:
            oldest_file = min(records_files, key=os.path.getctime)
            os.remove(oldest_file)
            records_files.remove(oldest_file)

    def write_record_to_file(self, file_path: str) -> None:
        """Write record content to file_path.

        Args:
            file_path (str): file path for the record file
        """
        with open(file_path, 'w') as f:
            f.write(self.__record_content)

    def reset_record_file(self) -> None:
        """Reset the record file. """
        self.__record_content = ""
        self.__record_content += f"{self.__level_filename}\n"
        self.__record_content += f"{self.__time_for_game}\n"
        self.__record_content += f"{self.__hearts_for_game}\n"
