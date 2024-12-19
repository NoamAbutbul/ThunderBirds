"""
    File to define the pause menu output.
"""


from src.io.menus import Menu
from src.io.output import OutputInterface
from src.io.input import InputInterface
from src.game_mechanics.status import Status


class PauseMenu(Menu):
    """Represent a pause menu.

    Attributes:
        output_manager (OutputInterface): output manager for the game
        input_manager (InputInterface): input manager for the game
        continue_play (str): continue play message
        exit (str): exit message
        hook (Callable): hook callable for the input handling
        status (Status): status of the game
    """

    def __init__(self, output_manager: OutputInterface, input_manager: InputInterface) -> None:
        """Initializes a new instance of the PauseMenu class.

        Args:
            output_manager (OutputInterface): output manager for the game
            input_manager (InputInterface): input manager for the game
        """
        super().__init__(output_manager, input_manager)
        self.__continue_play: str = "press Enter to continue play the game"
        self.__exit: str = "press Esc to exit"

    def show(self) -> None:
        """Show the pause menu to the client. """
        self.output_manager.clear_output()
        self.show_header()
        self.output_manager.print_at(
            self.__continue_play, 17, 28, self.output_manager.Color.GREEN)
        self.output_manager.print_at(
            self.__exit, 22, 38, self.output_manager.Color.RED)

    def show_header(self) -> None:
        """Show the header of the pause menu. """
        self.output_manager.show_text_animation(
            "Pause", 29, 8, 0.05, self.output_manager.Color.CYAN)

    def activate(self) -> Status:
        """Activate the pause menu.
            start listen to user input and handle it.

        Returns:
            Status: status for user input
        """
        self.status = Status.NULL
        self.show()

        buttons = self.input_manager.get_buttons()

        def handle_input(key: str) -> None:
            """Callback to handle user input.

            Args:
                key (str): key from the user input
            """
            statuses = {
                buttons.ENTER.value: Status.RESUME,
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
        """Deactivate the pause menu.
            release all resources.
        """
        self.input_manager.stop_listening(self.hook)
        self.output_manager.clear_output()
