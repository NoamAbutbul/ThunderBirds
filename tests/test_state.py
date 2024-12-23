"""
    File to test the State class.
"""

# autopep8: off
import pytest
from src.logger import logger
from src.configuration_files import ROWS, COLS
from src.game_mechanics.state import State
from src.game_pieces import LogicSymbol, GameObject, Point, Direction, MoveStatus, GameObjectType
from src.game_pieces.game_objects import Ship, Block, Wall, Portal


@pytest.fixture(autouse=False)
def clear_log():
    """Clear logger before the test. """
    logger.clear()


@pytest.fixture
def state_instance() -> State:
    """Fixture to create a State instance.

    Returns:
        State: State instance
    """
    return State()


@pytest.fixture
def init_state(state_instance: State) -> tuple[GameObject]:
    """Init state game for help testing.

    Args:
        state_instance (State): state instance fixture

    Returns:
        tuple[GameObject]: big ship, small ship, block numbers, block letters, portal
    """
    state_instance.init_blank_board()
    big_ship_location = [Point(2, 3), Point(3, 3), Point(4, 3), Point(5, 3)]
    big_ship_object = Ship(big_ship_location, LogicSymbol.BIG_SHIP.value, Ship.BIG_SHIP_MASS)
    state_instance.put_object(big_ship_object)
    small_ship_location = [Point(12, 24), Point(12, 25)]
    small_ship_object = Ship(small_ship_location, LogicSymbol.SMALL_SHIP.value, Ship.SMALL_SHIP_MASS)
    state_instance.put_object(small_ship_object)
    block_numbers_location = [Point(5, 4), Point(5, 5)]
    block_numbers_object = Block(block_numbers_location, '7', len(block_numbers_location))
    state_instance.put_object(block_numbers_object)
    block_letters_location = [Point(10, 23), Point(11, 23), Point(13, 23), Point(14, 23)]
    block_letters_object = Block(block_letters_location, 'R', len(block_letters_location))
    state_instance.put_object(block_letters_object)
    portal_location = [Point(12, 26)]
    portal_object = Portal(portal_location, LogicSymbol.PORTAL.value)
    state_instance.put_object(portal_object)
    state_instance.objects += [big_ship_object, small_ship_object, block_numbers_object, block_letters_object, portal_object]
    logger.debug(state_instance)
    return big_ship_object, small_ship_object, block_numbers_object, block_letters_object, portal_object


@pytest.fixture
def all_directions() -> list[Direction]:
    """All directions fixture.

    Returns:
        list[Direction]: all directions
    """
    all_directions = [direction for direction in Direction]
    return all_directions


def test_init_blank_board(state_instance: State) -> None:
    """Test init_blank_board function.

    Args:
        state_instance (State): state instance fixture
    """
    state_instance.init_blank_board()
    for row in range(ROWS):
        for col in range(COLS):
            conditions = {
                (col == 0) or (col == COLS - 1): LogicSymbol.WALL.value,
                (row == 0): LogicSymbol.WALL.value,
                (row == ROWS - 1): LogicSymbol.WALL.value
            }
            excepted_value = conditions.get(True, LogicSymbol.BLANK.value)
            assert state_instance.board[row][col] == excepted_value

def test_init_player(state_instance: State, init_state: tuple[GameObject]) -> None:
    """Testing init_player function.

    Args:
        state_instance (State): state instance fixture
        init_state (tuple[GameObject]): big ship, small ship, block numbers, block letters, portal 
    """
    assert (state_instance.current_player == None)
    state_instance.init_player()
    assert (state_instance.current_player.symbol == LogicSymbol.BIG_SHIP.value)


def test_switch_current_player(state_instance: State, init_state: tuple[GameObject]) -> None:
    """Testing switch_current_player function.

    Args:
        state_instance (State): state instance fixture
        init_state (tuple[GameObject]): big ship, small ship, block numbers, block letters, portal 
    """
    state_instance.init_player()
    state_instance.switch_current_player()
    assert (state_instance.current_player.symbol == LogicSymbol.SMALL_SHIP.value)
    state_instance.switch_current_player()
    assert (state_instance.current_player.symbol == LogicSymbol.BIG_SHIP.value)


def test_put_object(state_instance: State) -> None:
    """Testing put_object function.

    Args:
        state_instance (State): state instance fixture
    """
    location = [Point(1, 2), Point(2, 2), Point(3, 2), Point(2, 3)]
    big_ship_object = Ship(location, LogicSymbol.BIG_SHIP.value, Ship.BIG_SHIP_MASS)
    state_instance.init_blank_board()
    state_instance.put_object(big_ship_object)
    excepted_symbols = {
        (1, 2): big_ship_object.symbol,
        (2, 2): big_ship_object.symbol,
        (3, 2): big_ship_object.symbol,
        (2, 3): big_ship_object.symbol
    }
    for row in range(len(state_instance.board)):
        for col in range(len(state_instance.board[row])):
            excepted_symbol = excepted_symbols.get((row, col), None)
            assert ((state_instance.board[row][col] == excepted_symbol) or (state_instance.board[row][col] != big_ship_object.symbol))


def test_get_game_object_by_symbol(state_instance: State, init_state: tuple[GameObject]) -> None:
    """Testing get_game_object_by_symbol function.

    Args:
        state_instance (State): state instance fixture
        init_state (tuple[GameObject]): big ship, small ship, block numbers, block letters, portal
    """
    big_ship_object, _, _, _, _ = init_state
    assert (state_instance.get_game_object_by_symbol(LogicSymbol.BIG_SHIP.value) == big_ship_object)


def test_get_game_objects_in_my_direction(state_instance: State, init_state: tuple[GameObject]) -> None:
    """Testing get_game_objects_in_my_direction function.

    Args:
        state_instance (State): state instance fixture
        init_state (tuple[GameObject]): big ship, small ship, block numbers, block letters, portal
    """
    big_ship_object, small_ship_object, block_numbers_object, _, _ = init_state
    game_objects_in_my_direction = state_instance.get_game_objects_in_my_direction(big_ship_object, Direction.RIGHT)
    assert small_ship_object not in game_objects_in_my_direction
    assert block_numbers_object in game_objects_in_my_direction
    assert big_ship_object not in game_objects_in_my_direction

    game_objects_in_my_direction = state_instance.get_game_objects_in_my_direction(block_numbers_object, Direction.LEFT)
    assert big_ship_object in game_objects_in_my_direction
    assert small_ship_object not in game_objects_in_my_direction
    assert block_numbers_object not in game_objects_in_my_direction

    game_objects_in_my_direction = state_instance.get_game_objects_in_my_direction(block_numbers_object, Direction.UP)
    assert small_ship_object not in game_objects_in_my_direction
    assert big_ship_object not in game_objects_in_my_direction
    assert block_numbers_object not in game_objects_in_my_direction
    assert game_objects_in_my_direction == []

    game_objects_in_my_direction = state_instance.get_game_objects_in_my_direction(big_ship_object, Direction.UP)
    assert small_ship_object not in game_objects_in_my_direction
    assert block_numbers_object not in game_objects_in_my_direction
    assert big_ship_object not in game_objects_in_my_direction

    game_objects_in_my_direction = state_instance.get_game_objects_in_my_direction(small_ship_object, Direction.DOWN)
    assert big_ship_object not in game_objects_in_my_direction
    assert small_ship_object not in game_objects_in_my_direction
    assert block_numbers_object not in game_objects_in_my_direction












