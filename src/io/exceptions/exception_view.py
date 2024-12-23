"""
    File to define the ExceptionView class, to handle showing exceptions to client.
"""


from src.io.output import OutputInterface


class ExceptionView:
    """Represent a exception view.

    Attributes:
        output_manager (OutputInterface): output manager for the game
        message (str): exception message
    """

    def __init__(self, output_manager: OutputInterface, message: str) -> None:
        """Initializes a new instance of the ExceptionView class.

        Args:
            output_manager (OutputInterface): output manager for the game
            message (str): exception message
        """
        self.__output_manager: OutputInterface = output_manager
        self.__message: str = message

    def show(self) -> None:
        """Show the exception view. """
        self.__output_manager.clear_output()
        self.__output_manager.print_at(
            self.__message, 15, 5, self.__output_manager.Color.RED)
