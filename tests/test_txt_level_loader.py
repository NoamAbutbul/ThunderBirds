"""
    File to test the TxtLevelLoader class.
"""


# autopep8: off
import pytest
import random
from src.logger import logger
from src.configuration_files import ROWS, COLS
from src.game_pieces import LogicSymbol
from src.game_mechanics.level.txt_level_loader import TxtLevelLoader
from src.game_mechanics.level.level_loader_exception import LevelLoaderError


RANDOM_LEVEL_PATH = r"tests/demo_levels/random.level.txt"


@pytest.fixture(autouse=True)
def clear_log():
    """Clear logger before the test. """
    logger.clear()

@pytest.fixture
def txt_loader_instance() -> TxtLevelLoader:
    """Fixture to create a txt level loader instance.

    Returns:
        TxtLevelLoader: txt level loader instance
    """
    return TxtLevelLoader()


def create_valid_random_level() -> None:
    """Creating a valid random level to test the load level. """
    random_level = []
    symbols = LogicSymbol.all_values()
    symbols.remove(LogicSymbol.WALL.value)
    symbols.remove(LogicSymbol.BIG_SHIP.value)
    symbols.remove(LogicSymbol.SMALL_SHIP.value)
    symbols.remove(LogicSymbol.PORTAL.value)

    for row in range(ROWS):
        new_row = []
        for col in range(COLS):
            if (row == 0) or (row == ROWS - 1) or (col == 0) or (col == COLS - 1):
                new_row.append(LogicSymbol.WALL.value)
            else:
                new_row.append(random.choice(symbols))
        random_level.append(new_row)

    random_level[3][3] = LogicSymbol.BIG_SHIP.value
    random_level[4][3] = LogicSymbol.BIG_SHIP.value
    random_level[3][4] = LogicSymbol.BIG_SHIP.value
    random_level[4][4] = LogicSymbol.BIG_SHIP.value
    random_level[8][8] = LogicSymbol.SMALL_SHIP.value
    random_level[8][9] = LogicSymbol.SMALL_SHIP.value
    random_level[20][45] = LogicSymbol.PORTAL.value

    with open(RANDOM_LEVEL_PATH, 'w') as file:
        rows_str = [''.join(map(str, row)) for row in random_level]
        file.write('\n'.join(rows_str))

def test_load_level_by_path(txt_loader_instance: TxtLevelLoader) -> None:
    """Testing load_level_by_path function.

    Args:
        txt_loader_instance (TxtLevelLoader): txt loader instance fixture
    """
    with pytest.raises(LevelLoaderError):
        txt_loader_instance.load_level_by_path(None)
        txt_loader_instance.load_level_by_path(r"")
        txt_loader_instance.load_level_by_path(r"some_path")
        txt_loader_instance.load_level_by_path(r"tests/demo_levels/invalid1.level.txt")
        txt_loader_instance.load_level_by_path(r"tests/demo_levels/invalid2.level.txt")
        txt_loader_instance.load_level_by_path(r"tests/demo_levels/invalid3.level.txt")
        txt_loader_instance.load_level_by_path(r"tests/demo_levels/invalid4.level.txt")
    txt_loader_instance.load_level_by_path(r"tests/demo_levels/valid1.level.txt")
    create_valid_random_level()
    txt_loader_instance.load_level_by_path(RANDOM_LEVEL_PATH)

