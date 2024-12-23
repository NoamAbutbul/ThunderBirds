"""
    File to test Ship class.
"""


import pytest
from src.game_pieces import LogicSymbol, Point
from src.game_pieces.game_objects import Ship
from src.game_pieces.game_objects.ship.ship_exception import ShipError


def test_ship_init() -> None:
    """Test Ship.__init__ function. """

    with pytest.raises(ShipError):
        location = [Point(4, 4), Point(3, 8)]
        Ship(location, LogicSymbol.BIG_SHIP.value)

        location = [Point(4, 4), Point(3, 8), Point(1, 6), Point(8, 4)]
        Ship(location, LogicSymbol.BIG_SHIP.value)

        Ship([], LogicSymbol.BIG_SHIP.value)
        Ship([1, 2, 3, 4], LogicSymbol.BIG_SHIP.value)

    location = [Point(3, 3), Point(4, 3), Point(3, 4), Point(4, 4)]
    Ship(location, LogicSymbol.BIG_SHIP.value)
