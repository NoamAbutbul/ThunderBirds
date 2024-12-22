"""
    File to define the start menu output.
"""


from typing import Callable
from src.io.menus import Menu
from src.io.output import OutputInterface
from src.io.input import InputInterface
from src.io.pointer import Pointer
from src.game_mechanics.status import Status


class StartMenu(Menu):
    """Represent a start menu.

    Attributes:
        output_manager (OutputInterface): output manager for the game
        input_manager (InputInterface): input manager for the game
        callbacks (list[(int, int, Callable)]): positions and functions list to pointed to
        pointer (Pointer): pointer for the options
        new_game (str): new game message
        records (str): records menu message
        rules (str): rules menu message
        exit (str): exit message
        hook (Callable): hook callable for the input handling
        status (Status): status of the game
    """

    NEW_GAME_X_POSITION = 20
    RECORDS_X_POSITION = 22
    RULES_X_POSITION = 24
    EXIT_GAME_X_POSITION = 26
    ELEMENT_OPTIONS_Y_POSITION = 41

    def __init__(self, output_manager: OutputInterface, input_manager: InputInterface) -> None:
        """Initializes a new instance of the StartMenu class.

        Args:
            output_manager (OutputInterface): output manager for the game
            input_manager (InputInterface): input manager for the game
        """
        super().__init__(output_manager, input_manager)
        self.__callbacks: list[(int, int, Callable)] = []
        self.init_callbacks()
        self.__pointer: Pointer = Pointer(
            output_manager, input_manager, self.__callbacks)
        self.__new_game: str = "new game"
        self.__records: str = "records"
        self.__rules: str = "rules"
        self.__exit: str = "exit"

    def init_callbacks(self) -> None:
        """Init callbacks list for the pointer. """
        self.__callbacks.append((StartMenu.NEW_GAME_X_POSITION,
                                StartMenu.ELEMENT_OPTIONS_Y_POSITION, (self.change_status, (Status.NEW_GAME,), {})))
        self.__callbacks.append((StartMenu.RECORDS_X_POSITION,
                                StartMenu.ELEMENT_OPTIONS_Y_POSITION, (self.change_status, (Status.RECORDS,), {})))
        self.__callbacks.append((StartMenu.RULES_X_POSITION,
                                StartMenu.ELEMENT_OPTIONS_Y_POSITION, (self.change_status, (Status.RULES,), {})))
        self.__callbacks.append((StartMenu.EXIT_GAME_X_POSITION,
                                StartMenu.ELEMENT_OPTIONS_Y_POSITION, (self.change_status, (Status.EXIT,), {})))

    def change_status(self, status: Status) -> None:
        """Change current game status.

        Args:
            status (Status): new status
        """
        self.status = status

    def show(self) -> None:
        """Show the start menu to the client. """
        self.output_manager.clear_output()
        self.show_header()
        self.output_manager.print_at(self.__new_game, StartMenu.NEW_GAME_X_POSITION,
                                     StartMenu.ELEMENT_OPTIONS_Y_POSITION, self.output_manager.Color.GREEN)
        self.output_manager.print_at(self.__records, StartMenu.RECORDS_X_POSITION,
                                     StartMenu.ELEMENT_OPTIONS_Y_POSITION, self.output_manager.Color.YELLOW)
        self.output_manager.print_at(self.__rules, StartMenu.RULES_X_POSITION,
                                     StartMenu.ELEMENT_OPTIONS_Y_POSITION, self.output_manager.Color.CYAN)
        self.output_manager.print_at(self.__exit, StartMenu.EXIT_GAME_X_POSITION,
                                     StartMenu.ELEMENT_OPTIONS_Y_POSITION, self.output_manager.Color.RED)
        self.__pointer.show()

    def show_header(self) -> None:
        """Showing the header of the start menu. """
        self.output_manager.show_text_animation(
            "Thunder", 21, 5, 0.04, self.output_manager.Color.YELLOW)
        self.output_manager.show_text_animation(
            "Birds", 30, 11, 0.04, self.output_manager.Color.LIGHT_RED)

    def activate(self) -> Status:
        """Activate the start menu.
            start listen to user input and handle it.

        Returns:
            Status: status for the user input
        """
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

    def deactivate(self) -> None:
        """Deactivate the start menu.
            release all resources.
        """
        self.input_manager.stop_listening(self.hook)
        self.output_manager.clear_output()
        self.__pointer.deactivate()
