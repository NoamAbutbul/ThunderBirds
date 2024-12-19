"""
    File to define the state of the game,
    the logic of the game define in this file.
"""


from src.logger import logger
from src.game_pieces import LogicSymbol, GameObjectType, GameObject, Point, Direction, MoveStatus
from src.game_pieces.game_objects import Ship, Block, Wall, Portal
from src.configuration_files import ROWS, COLS


class State:
    """Represent a state in the game.

    Attributes:
        board (list[list[str]]): the logic board
        game_objects (list[GameObject]): the game objects
        current_player (GameObject): the current player pointer
        ship_amount (int): the ship amount on the board
    """

    def __init__(self, board: list[list[str]] = None, game_objects: list[GameObject] = None) -> None:
        """Initializes a new instance of the State class.

        Args:
            board (list[list[str]], optional): logic board. Defaults to None.
            game_objects (list[GameObject], optional): game objects. Defaults to None.
        """
        self.__board: list[list[str]] = board
        if game_objects != None:
            self.__game_objects: list[GameObject] = game_objects
        else:
            self.__game_objects: list[GameObject] = []
        self.__current_player: GameObject = None
        self.__ships_amount: int = 0

    def init_new_game(self) -> None:
        """Init new game after the board is ready. """
        self.init_player()

    @property
    def board(self) -> list[list[str]]:
        copy_board = [[None] * COLS for _ in range(ROWS)]
        for row in range(ROWS):
            for col in range(COLS):
                copy_board[row][col] = self.__board[row][col]
        return copy_board

    @board.setter
    def board(self, board: list[list[str]]) -> None:
        self.__board = [[None] * COLS for _ in range(ROWS)]
        for row in range(ROWS):
            for col in range(COLS):
                self.__board[row][col] = board[row][col]

    @property
    def objects(self) -> list[GameObject]:
        copy_objects = []
        for obj in self.__game_objects:
            copy_objects.append(obj)
        return copy_objects

    @objects.setter
    def objects(self, objects: list[GameObject]) -> None:
        self.__game_objects = []
        for obj in objects:
            self.__game_objects.append(obj)

    @property
    def current_player(self) -> GameObject:
        return self.__current_player

    @property
    def ship_amount(self) -> int:
        return self.__ships_amount

    def init_blank_board(self) -> None:
        """Init blank board (with walls) in size of ROWS*COLS. """
        self.__game_objects = []
        self.__board = []
        wall_game_object = Wall([], LogicSymbol.WALL.value)
        for row in range(ROWS):
            new_row = []
            for col in range(COLS):
                if (col == 0) or (col == COLS - 1) or (row == 0) or (row == ROWS - 1):
                    new_row.append(LogicSymbol.BLANK.value)
                    wall_game_object.add_point(Point(row, col))
                else:
                    new_row.append(LogicSymbol.BLANK.value)
            self.__board.append(new_row)

        self.__game_objects.append(wall_game_object)
        self.put_objects(self.__game_objects)

    def put_object(self, game_object: GameObject) -> None:
        """Put object in the board by it location.

        Args:
            game_object (GameObject): object to put
        """
        if game_object.type in [GameObjectType.BIG_SHIP, GameObjectType.SMALL_SHIP]:
            self.__ships_amount += 1
        for point in game_object.location:
            self.__board[point.x][point.y] = game_object.symbol

    def put_objects(self, game_objects: list[GameObject]) -> None:
        """Put object list in the board.

        Args:
            game_objects (list[GameObject]): objects to put
        """
        for game_object in game_objects:
            self.put_object(game_object)

    def move_game_object_to_first(self, game_object: GameObject) -> None:
        """Move game object to the first in the game_objects list.

        Args:
            game_object (GameObject): game object to move to first
        """
        if game_object in self.__game_objects:
            self.__game_objects.remove(game_object)
            self.__game_objects.insert(0, game_object)

    def load_board(self, board: list[list[str]]) -> None:
        """Loading board to self instance.

        Args:
            board (list[list[str]]): board to load
        """
        logger.info("Loading board to the model...")
        logger.log_board(msg="The board to load", board=board)

        self.__ships_amount = 0
        self.__board = [[LogicSymbol.BLANK.value] * COLS for _ in range(ROWS)]  # noqa
        self.__game_objects: list[GameObject] = []

        symbol_map = {
            LogicSymbol.BIG_SHIP.value: Ship,
            LogicSymbol.SMALL_SHIP.value: Ship,
            LogicSymbol.WALL.value: Wall,
            LogicSymbol.PORTAL.value: Portal
        }

        for symbol in LogicSymbol.BLOCK_LETTERS.value + LogicSymbol.BLOCK_NUMBERS.value:
            symbol_map[symbol] = Block

        dict_of_game_object: dict = self.get_game_objects_from_matrix(board)
        for symbol, location in dict_of_game_object.items():
            game_object_class = symbol_map[symbol]
            game_object = game_object_class(symbol=symbol, location=location)
            if game_object_class == Block:
                game_object.mass = len(location)
            self.__game_objects.append(game_object)

        self.put_objects(self.__game_objects)
        logger.log_board(msg="The board that loaded", board=self.__board)

    def get_game_objects_from_matrix(self, matrix: list[list[str]]) -> dict[str, list[Point]]:
        """Gets a matrix and build a dictionary with all game objects in the matrix.

        Args:
            matrix (list[list[str]]): board matrix

        Returns:
            dict[str, list[Point]]: all game objects in the matrix. key is the game object symbol
        """
        dict_of_game_objects: dict = {}
        for row in range(ROWS):
            for col in range(COLS):
                symbol = matrix[row][col]
                if symbol != LogicSymbol.BLANK.value:
                    if symbol not in dict_of_game_objects:
                        dict_of_game_objects[symbol] = []
                    dict_of_game_objects[symbol].append(Point(row, col))
        return dict_of_game_objects

    def init_player(self) -> None:
        """Init current_player to the big ship for the start game.
            Note - if the big ship not on the board, init current_player to None.
        """
        self.__current_player = self.get_game_object_by_symbol(
            LogicSymbol.BIG_SHIP.value)

    def switch_current_player(self) -> None:
        """Switching the current_player to the other player. """
        if self.__current_player == self.get_game_object_by_symbol(LogicSymbol.BIG_SHIP.value):
            self.__current_player = self.get_game_object_by_symbol(
                LogicSymbol.SMALL_SHIP.value)
        elif self.__current_player == self.get_game_object_by_symbol(LogicSymbol.SMALL_SHIP.value):
            self.__current_player = self.get_game_object_by_symbol(
                LogicSymbol.BIG_SHIP.value)

    def get_game_object_by_symbol(self, logic_symbol: str) -> GameObject:
        """Get game object by its symbol from the game object list.

        Args:
            logic_symbol (str): logic symbol value of the object to find

        Returns:
            GameObject: object that found
        """
        if logic_symbol == LogicSymbol.BLANK.value:
            return LogicSymbol.BLANK.value
        ret_game_object = None
        for game_object in self.__game_objects:
            if game_object.symbol == logic_symbol:
                ret_game_object = game_object
        return ret_game_object

    def can_move(self, root_object: GameObject, power: list[int], game_object: GameObject, direction: Direction, need_to_move: list[GameObject]) -> MoveStatus:
        """Gets a game object that want to move in some direction
            and return status for that move
            and build a list of all game objects that need to move with it.

        Args:
            root_object (GameObject): root object that active this function
            power (list[int]): list with one value: current power mass
            game_object (GameObject): current game object
            direction (Direction): move direction
            need_to_move (list[GameObject]): list of all game objects that need to move in that direction

        Returns:
            MoveStatus: move status for this case
        """
        neighbors = self.get_game_objects_in_my_direction(
            game_object, direction)
        if neighbors == []:
            need_to_move.insert(0, game_object)
            self.check_carry_game_objects_above(
                root_object, power, game_object, direction, need_to_move)
            return MoveStatus.CAN_MOVE

        for neighbor in neighbors:
            if neighbor == root_object:
                continue
            neighbor_move_status = neighbor.can_be_pushed(
                root_object, power, game_object, direction)
            if neighbor_move_status == MoveStatus.CANNOT_MOVE:
                return MoveStatus.CANNOT_MOVE
            elif neighbor_move_status == MoveStatus.REDUCE_LIFE:
                if self.validate_lose(neighbors):
                    return MoveStatus.REDUCE_LIFE
            elif neighbor_move_status == MoveStatus.VICTORY:
                return MoveStatus.VICTORY

            neighbor_move_status = self.can_move(
                root_object, power, neighbor, direction, need_to_move)

            if neighbor_move_status != MoveStatus.CAN_MOVE:
                return neighbor_move_status

        need_to_move.insert(0, game_object)
        self.check_carry_game_objects_above(
            root_object, power, game_object, direction, need_to_move)
        return MoveStatus.CAN_MOVE

    def check_carry_game_objects_above(self, root_object: GameObject, power: list[int], game_object: GameObject, direction: Direction, need_to_move: list[GameObject]) -> None:
        """Checking if need to add all game objects above to the movement.

        Args:
            root_object (GameObject): root object that active can_move function
            power (list[int]): list with one value: current power mass
            game_object (GameObject): current game object
            direction (Direction): move direction
            need_to_move (list[GameObject]): list of all game objects that need to move in that direction
        """
        if direction in [Direction.UP, direction.DOWN]:
            return
        game_objects_above = self.get_game_objects_in_my_direction(
            game_object, Direction.UP)

        for game_object_above in game_objects_above:
            move_status = game_object_above.can_be_pushed(
                root_object, power, game_object_above, direction)
            if (game_object_above != game_object) and (move_status == MoveStatus.CAN_MOVE) and (game_object_above not in need_to_move):
                self.can_move(root_object, power,
                              game_object_above, direction, need_to_move)

    def validate_lose(self, game_objects_in_my_direction: list[GameObject]) -> bool:
        """Validate lose case by checking game_objects_in_my_direction list.

        Args:
            game_objects_in_my_direction (list[GameObject]): list to validate

        Returns:
            bool: True - if its really lose case, else False
        """
        is_lose = False
        for game_object_in_my_direction in game_objects_in_my_direction:
            if len(game_objects_in_my_direction) == 1:
                if game_object_in_my_direction.type in [GameObjectType.BIG_SHIP, GameObjectType.SMALL_SHIP]:
                    is_lose = True
        return is_lose

    def get_all_game_objects_in_my_direction(self, game_object: GameObject, direction: Direction, game_objects_in_my_direction: list[GameObject], objects_checked: list[GameObject] = []) -> None:
        """Get all game objects in direction of specific game_object.

        Args:
            game_object (GameObject): game object to check
            direction (Direction): direction to check
            game_objects_in_my_direction (list[GameObject]): list with all game objects that in the direction of game_object
            objects_checked (list[GameObject], optional): game objects that already checked. Defaults to [].
        """
        game_objects_in_direction_of_game_object = self.get_game_objects_in_my_direction(
            game_object, direction)
        if game_objects_in_direction_of_game_object == []:
            return
        game_objects_in_my_direction += game_objects_in_direction_of_game_object
        for game_object_in_direction in game_objects_in_my_direction:
            if game_object in objects_checked:
                continue
            objects_checked.append(game_object_in_direction)
            self.get_all_game_objects_in_my_direction(
                game_object_in_direction, direction, game_objects_in_my_direction, objects_checked)

    def get_game_objects_in_my_direction(self, game_object: GameObject, direction: Direction) -> list[GameObject]:
        """Get list of game objects that stand in my direction.

        Args:
            game_object (GameObject): game object to check for
            direction (Direction): direction to check for

        Returns:
            list[GameObject]: all game objects that stand in my direction
        """
        game_objects_in_my_direction: list[GameObject] = []
        for point in game_object.location:
            point_in_my_direction = point + direction.value
            obj_in_my_direction = self.get_game_object_by_point(
                point_in_my_direction)
            if (obj_in_my_direction != LogicSymbol.BLANK.value) \
                    and (obj_in_my_direction != game_object):
                game_objects_in_my_direction.append(obj_in_my_direction)
        game_objects_in_my_direction = list(set(game_objects_in_my_direction))
        return game_objects_in_my_direction

    def move_game_object(self, symbol: str, source: list[Point], dest: list[Point]) -> None:
        """Move game object on the board.

        Args:
            symbol (str): symbol of the object
            source (list[Point]): source location of the object
            dest (list[Point]): destination location of the object
        """
        source_set = set(source)
        dest_set = set(dest)
        source_diff = source_set.difference(dest_set)
        dest_diff = dest_set.difference(source_set)
        for point in source_diff:
            self.__board[point.x][point.y] = LogicSymbol.BLANK.value
        for point in dest_diff:
            self.__board[point.x][point.y] = symbol

    def get_game_object_by_point(self, point: Point) -> GameObject:
        """Get game object by its one point location.

        Args:
            point (Point): one point location on the board

        Returns:
            GameObject: the game object that exist in the point
        """
        sign_on_board = self.__board[point.x][point.y]
        game_object = self.get_game_object_by_symbol(sign_on_board)
        return game_object

    def __str__(self) -> str:
        """Get state description.

        Returns:
            str: state description
        """
        ret_str = "\n"
        for row in range(ROWS):
            for col in range(COLS):
                ret_str += self.__board[row][col] + ''
            ret_str += "\n"

        ret_str += "\n\n"
        ret_str += f"Objects: {self.__game_objects}"
        return ret_str
