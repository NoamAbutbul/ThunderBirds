"""This file is made for making game_mechanics as a package. """


import sys
from src.exceptions import BasicException


def cannot_run_game(exception: BasicException) -> None:
    """Show exception message and close the game.

    Args:
        exception (BasicException): exception to show
    """
    import colorama
    colorama.init()
    print(colorama.Fore.RED + f"The game cannot run due to error: {exception}")
    sys.exit()
