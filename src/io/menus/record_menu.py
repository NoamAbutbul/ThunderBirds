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
        self.output_manager.clear_output()
        self.show_header()
        self.show_records_games()
        self.__pointer.show()
        self.output_manager.print_at(
            self.__exit, 34, 37, self.output_manager.Color.RED)

    def show_header(self) -> None:
        """Showing the header of the game. """
        self.output_manager.show_text_animation(
            "Records", 21, 8, 0.05, self.output_manager.Color.CYAN)

    def show_records_games(self) -> None:
        """Showing all records games available. """
        line_index = RecordMenu.FILENAME_X_POSITION
        for filename in self.__records_filenames:
            self.output_manager.print_at(os.path.basename(
                filename), line_index, RecordMenu.FILENAME_Y_POSITION, self.output_manager.Color.YELLOW)

    def activate(self) -> Status:
        """Activate the record menu.
            start listen to user input and handle it.

        Returns:
            Status: status for the user input
        """
        self.init_records_files()
        self.init_callbacks_and_pointer()
        self.status = Status.NULL
        self.show()
        self.__pointer.activate()
        buttons = self.input_manager.get_buttons()

        def handle_input(key: str) -> None:
            """Callback to handle user input.

            Args:
                key (str): key from the user input
            """
            statuses = {
                buttons.EXIT.value: Status.EXIT
            }
            if key in statuses:
                self.status = statuses[key]

        self.hook = self.input_manager.start_listening(handle_input)

        while (self.status == Status.NULL):
            pass

        self.deactivate()
        return self.status

    def play_record(self, record_name: str) -> None:
        """Play record selected.

        Args:
            record_name (str): record name to play
        """
        logger.info(f"Playing record: {record_name}")
        self.current_record_file = record_name
        self.status = Status.PLAY_RECORD

    def deactivate(self) -> None:
        """Deactivate the record menu. 
            release all resources.
        """
        self.input_manager.stop_listening(self.hook)
        self.output_manager.clear_output()
        self.__pointer.deactivate()
