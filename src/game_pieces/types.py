"""
    File to define the available types for GameObject.
"""


from enum import Enum
from src.game_pieces.symbols import LogicSymbol


class GameObjectType(Enum):
    """Enum that represent all game types. """
    BIG_SHIP = "Big Ship"
    SMALL_SHIP = "Small Ship"
    BLOCK_NUMBERS = "Block Numbers"
    BLOCK_LETTERS = "Block Letters"
    WALL = "Wall"
    PORTAL = "Portal"

    @staticmethod
    def get_type_by_symbol(symbol: str) -> "GameObjectType":
        """Get game object type by its symbol.

        Args:
            symbol (str): game object symbol

        Returns:
            GameObjectType: game object type
        """
        symbol_map = {
            LogicSymbol.BIG_SHIP.value: GameObjectType.BIG_SHIP,
            LogicSymbol.SMALL_SHIP.value: GameObjectType.SMALL_SHIP,
            LogicSymbol.WALL.value: GameObjectType.WALL,
            LogicSymbol.PORTAL.value: GameObjectType.PORTAL,
        }
        for sign in LogicSymbol.BLOCK_LETTERS.value + LogicSymbol.BLOCK_NUMBERS.value:
            symbol_map[sign] = (
                GameObjectType.BLOCK_LETTERS if sign in LogicSymbol.BLOCK_LETTERS.value else GameObjectType.BLOCK_NUMBERS)

        return symbol_map[symbol]
