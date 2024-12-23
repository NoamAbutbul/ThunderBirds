"""
    File to test the Portal class.
"""

import pytest
from src.game_pieces import LogicSymbol, Point
from src.game_pieces.game_objects.portal import Portal
from src.game_pieces.game_objects.portal.portal_exception import PortalError


def test_portal_init() -> None:
    """Test portal.__init__ function. """

    with pytest.raises(PortalError):
        Portal([], LogicSymbol.PORTAL.value)
        Portal([Point(2, 3), Point(5, 8)], LogicSymbol.PORTAL.value)

    Portal([Point(2, 3)], LogicSymbol.PORTAL.value)
