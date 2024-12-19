"""
    File to define the record menu output.
"""


import os
import glob
from typing import Callable
from src.io.menus import Menu
from src.io.output import OutputInterface
from src.io.input import InputInterface
from src.game_mechanics.status import Status
from src.io.pointer import Pointer
from src.logger import logger


class RecordMenu(Menu):
    """Represent a record menu.

    Attributes:
        output_manager (OutputInterface): output manager for the game
        input_manager (InputInterface): input manager for the game
        records_filenames (list[str]): all records filenames
        current_record_file (str): current record file
        callbacks (list[(int, int, Callable)]): positions and functions list to pointed to
        pointer (Pointer): pointer for the record
        exit (str): exit message
        hook (Callable): hook callable for the input handling
        status (Status): status of the game
    """

    RECORDS_PATH = r"records"
    FILENAME_X_POSITION = 18
    FILENAME_Y_POSITION = 38

    def __init__(self, output_manager: OutputInterface, input_manager: InputInterface) -> None:
        """Initializes a new instance of the RecordMenu class.

        Args:
            output_manager (OutputInterface): output manager for the game
            input_manager (InputInterface): input manager for the game
        """
        super().__init__(output_manager, input_manager)
        self.init_records_files()
        if len(self.__records_filenames) > 0:
            self.__current_record_file: str = self.__records_filenames[0]
        self.__callbacks: list[(int, int, Callable)] = []
        self.__pointer: Pointer = None
        self.init_callbacks_and_pointer()
        self.__exit: str = "press Esc to exit"

    @property
    def current_record_file(self) -> str:
        return self.__current_record_file

    @current_record_file.setter
    def current_record_file(self, value: str) -> None:
        self.__current_record_file = value

    def init_records_files(self) -> None:
        """Init records files from the dir path. """
        self.__records_filenames: list[str] = glob.glob(
            RecordMenu.RECORDS_PATH + "/")

    def init_callbacks_and_pointer(self) -> None:
        """Init pointer & callback list for the pointer. """
        self.__callbacks: list[(int, int, Callable)] = []
        file_index = RecordMenu.FILENAME_X_POSITION
        for filename in self.__records_filenames:
            callback = (file_index, RecordMenu.FILENAME_Y_POSITION,
                        (self.play_record, (filename,), {}))
            self.__callbacks.append(callback)
            file_index += 2
        self.__pointer: Pointer = Pointer(
            self.output_manager, self.input_manager, self.__callbacks)

    def show(self) -> None:
        """Show the record menu to the client. """
        # TODO -> implement
