"""
    File to define the games rules menu output.
"""


from src.game_consts import RULES
from src.io.menus import Menu
from src.io.output import OutputInterface
from src.io.input import InputInterface
from src.game_mechanics.status import Status


class RulesMenu(Menu):
    """Represent a rules menu.

    Attributes:
        output_manager (OutputInterface): output manager for the game
        input_manager (InputInterface): input manager for the game
        hook (Callable): hook callable for the input handling
        status (Status): status of the game
    """

    OUTPUT_WIDTH_SIZE = 96
    OUTPUT_HEIGHT_SIZE = 40

    def __init__(self, output_manager: OutputInterface, input_manager: InputInterface) -> None:
        """Initializes a new instance of the RulesMenu class.

        Args:
            output_manager (OutputInterface): output manager for the game
            input_manager (InputInterface): input manager for the game
        """
        super().__init__(output_manager, input_manager)

    def show(self) -> None:
        """Show the rules menu to the client. """
        self.output_manager.clear_output()
        self.output_manager.set_output_size(
            RulesMenu.OUTPUT_WIDTH_SIZE, RulesMenu.OUTPUT_HEIGHT_SIZE)
        self.output_manager.print_at(
            "Game Rules: ", 1, 43, self.output_manager.Color.CYAN)
        self.output_manager.print_at(RULES, 4, 1)
        self.output_manager.print_at(
            "Press Esc to return to start menu", 38, 34, self.output_manager.Color.GREEN)

    def activate(self) -> Status:
        """Activate the rules menu.
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
        """Deactivate the rules menu.
            release all resources.
        """
        self.input_manager.stop_listening(self.hook)
        self.output_manager.clear_output()
