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


@pytest.fixture(autouse=True)
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
    block_letters_location = [Point(10, 23), Point(11, 23), Point(12, 23), Point(13, 23), Point(14, 23)]
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


def test_move_game_object(state_instance: State, init_state: tuple[GameObject]) -> None:
    """Testing move_game_object function.

    Args:
        state_instance (State): state instance fixture
        init_state (tuple[GameObject]): big ship, small ship, block numbers, block letters, portal
    """
    big_ship_object, _, _, _, _ = init_state
    source_location = big_ship_object.copied_location
    dest_location = [Point(1, 3), Point(2, 3), Point(3, 3), Point(2, 4)]
    state_instance.move_game_object(big_ship_object.symbol, big_ship_object.location, dest_location)
    for point in source_location:
        if point != Point(2, 3) and point != Point(3, 3):
            assert state_instance.board[point.x][point.y] == LogicSymbol.BLANK.value
    for point in dest_location:
        assert state_instance.board[point.x][point.y] == LogicSymbol.BIG_SHIP.value


def test_get_game_object_by_point(state_instance: State, init_state: tuple[GameObject]) -> None:
    """Testing get_game_object_by_point function.

    Args:
        state_instance (State): state instance fixture
        init_state (tuple[GameObject]): big ship, small ship, block numbers, block letters, portal
    """
    big_ship_object, small_ship_object, block_numbers_object, block_letters_object, portal_object = init_state
    game_objects = {big_ship_object, small_ship_object, block_numbers_object, block_letters_object, portal_object}
    for game_object in game_objects:
        for point in game_object.location:
            assert state_instance.get_game_object_by_point(point) == game_object

    for row in range(ROWS):
        for col in range(COLS):
            current_point = Point(row, col)
            if any(current_point in game_object.location for game_object in game_objects):
                continue
            if (col == 0) or (col == COLS - 1) or (row == 0) or (row == ROWS - 1):
                assert state_instance.get_game_object_by_point(current_point).type == GameObjectType.WALL
                continue
            assert state_instance.get_game_object_by_point(current_point) == LogicSymbol.BLANK.value

def test_can_move(state_instance: State, init_state: tuple[GameObject]) -> None:
    """Testing can_move function.

    Args:
        state_instance (State): state instance fixture
        init_state (tuple[GameObject]): big ship, small ship, block numbers, block letters, portal
    """
    big_ship_object, small_ship_object, block_numbers_object, _, _ = init_state
    logger.log_board("board", state_instance.board)

    def assert_move_status(game_object: GameObject, direction: Direction, excepted_status: MoveStatus, excepted_need_to_move: list[GameObject] = None) -> None:
        """Helper function to assert can_move output function.

        Args:
            game_object (GameObject): game object to check
            direction (Direction): direction to check
            excepted_status (MoveStatus): excepted status output from can_move function
            excepted_need_to_move (list[GameObject], optional): excepted need_to_move list after can_move function. Defaults to None.
        """
        need_to_move: list[GameObject] = []
        move_status = state_instance.can_move(game_object, [game_object.mass], game_object, direction, need_to_move)
        assert move_status == excepted_status
        if excepted_need_to_move is not None:
            assert need_to_move == excepted_need_to_move

    assert_move_status(big_ship_object, Direction.LEFT, MoveStatus.CAN_MOVE, [big_ship_object])
    assert_move_status(big_ship_object, Direction.DOWN, MoveStatus.CAN_MOVE, [big_ship_object])
    assert_move_status(big_ship_object, Direction.UP, MoveStatus.CAN_MOVE, [big_ship_object])
    assert_move_status(big_ship_object, Direction.RIGHT, MoveStatus.CANNOT_MOVE)
    assert_move_status(small_ship_object, Direction.RIGHT, MoveStatus.VICTORY)
    assert_move_status(small_ship_object, Direction.DOWN, MoveStatus.CAN_MOVE, [small_ship_object])
    assert_move_status(small_ship_object, Direction.UP, MoveStatus.CAN_MOVE, [small_ship_object])
    assert_move_status(small_ship_object, Direction.LEFT, MoveStatus.CANNOT_MOVE)
    assert_move_status(block_numbers_object, Direction.DOWN, MoveStatus.CAN_MOVE, [block_numbers_object])
    assert_move_status(block_numbers_object, Direction.RIGHT, MoveStatus.CAN_MOVE, [block_numbers_object])
    assert_move_status(block_numbers_object, Direction.UP, MoveStatus.CAN_MOVE, [block_numbers_object])
    assert_move_status(block_numbers_object, Direction.LEFT, MoveStatus.CANNOT_MOVE)

    dest = [Point(6, 4), Point(7, 4), Point(8, 4), Point(9, 4)]
    state_instance.move_game_object(big_ship_object.symbol, big_ship_object.copied_location, dest)
    block_numbers_object.mass = big_ship_object.mass + 1
    assert_move_status(block_numbers_object, Direction.DOWN, MoveStatus.REDUCE_LIFE)








