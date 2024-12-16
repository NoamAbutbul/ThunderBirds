"""
    File to define the symbols in the game.
"""


import string
from enum import Enum
from src.configuration_files import GameObjectColor


class ViewSymbol(Enum):
    """Enum that represent view symbol of game object. """
    BIG_SHIP = "@"
    SMALL_SHIP = "%"
    WALL_VERTICAL = "?"  # TODO -> find the original symbol
    WALL_HORIZONTAL_UP = "?"  # TODO -> find the original symbol
    WALL_HORIZONTAL_DOWN = "?"  # TODO -> find the original symbol
    BLANK = " "
    PORTAL = "?"  # TODO -> find the original symbol
    BLOCK_LETTERS = list(string.ascii_letters)
    BLOCK_NUMBERS = [str(value) for value in range(10)]
    HEART = "<>"  # TODO -> find the original symbol
    POINTER = ">"  # TODO -> find the original symbol

    def get_value_by_logic_sign(logic_sign: str) -> str:
        """Gets logic sign and classify its to view symbol value.

        Args:
            logic_sign (str): sign to classify

        Returns:
            str: view symbol value
        """
        view_to_logic_symbol_dict = {
            LogicSymbol.WALL.value: ViewSymbol.WALL_VERTICAL.value,
            LogicSymbol.BLANK.value: ViewSymbol.BLANK.value,
            LogicSymbol.BIG_SHIP.value: ViewSymbol.BIG_SHIP.value,
            LogicSymbol.SMALL_SHIP.value: ViewSymbol.SMALL_SHIP.value,
            LogicSymbol.PORTAL.value: ViewSymbol.PORTAL.value,
        }
        ret_value = view_to_logic_symbol_dict.get(logic_sign, logic_sign)
        return ret_value


class LogicSymbol(Enum):
    """Enum that represent logic symbol of game object. """
    BIG_SHIP = '@'
    SMALL_SHIP = '$'
    WALL = '#'
    BLANK = ' '
    PORTAL = '+'
    BLOCK_LETTERS = list(string.ascii_letters)
    BLOCK_NUMBERS = [str(value) for value in range(10)]

    @staticmethod
    def all_values() -> list[str]:
        """Get all values of the LogicSymbol Enum.

        Returns:
            list[str]: all values
        """
        symbols = [s.value for s in LogicSymbol.__members__.values()]
        all_symbols_elements = []
        for sublist in symbols:
            if isinstance(sublist, list):
                all_symbols_elements += sublist
            else:
                all_symbols_elements.append(sublist)
        return all_symbols_elements
