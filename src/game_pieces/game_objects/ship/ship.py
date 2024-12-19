"""
    File to define the Ship game object.
"""


from src.game_consts import BIG_SHIP_SIZE, SMALL_SHIP_SIZE
from src.game_pieces.point import Point, Direction
from src.game_pieces.game_object import GameObject, GameObjectType, MoveStatus
from src.game_pieces.game_objects.ship.ship_exception import ShipSizeError, ShipLocationError


class Ship(GameObject):
    """Represent a ship object (inherits from GameObject).

    Attributes:
        location (list[Point]): location in the board
        symbol (str): symbol of the object
        mass (int): mass of the object
        direction (Direction): direction of the object
        type (GameObjectType): game object type
    """

    SMALL_SHIP_MASS, BIG_SHIP_MASS = 5, 10

    def __init__(self, location: list[Point] = None, symbol: str = None, mass: int = 0, direction: Direction = Direction.NULL) -> None:
        """Initializes a new instance of the Ship class.

        Args:
            location (list[Point], optional): location in the board. Defaults to None.
            symbol (str, optional): symbol of the object. Defaults to None.
            mass (int, optional): mass of the object. Defaults to 0.
            direction (Direction, optional): direction of the object. Defaults to Direction.NULL.
        """
        super().__init__(location, symbol, 0, direction)
        mass = Ship.SMALL_SHIP_MASS
        if self.type == GameObjectType.BIG_SHIP:
            mass = Ship.BIG_SHIP_MASS
        self.mass = mass

        self.size_validation()
        self.location_validation()

    def __str__(self) -> str:
        """Get ship object description.

        Returns:
            str: ship object description
        """
        return super().__str__()

    def can_be_pushed(self, root_pusher: GameObject, power: list[int], pusher: GameObject, direction: Direction) -> MoveStatus:
        """Checking if self can be pushed by root_pusher in some direction.

        Args:
            root_pusher (GameObject): root pusher that want to push
            power (list[int]): list with one value: current power mass
            pusher (GameObject): pusher game object
            direction (Direction): direction of pushing

        Returns:
            MoveStatus: status for that move
        """
        if root_pusher.type in [GameObjectType.BLOCK_LETTERS, GameObjectType.BLOCK_NUMBERS]:
            if direction == Direction.DOWN:
                if power[0] > self.mass:
                    return MoveStatus.REDUCE_LIFE

        if power[0] <= self.mass:
            return MoveStatus.CANNOT_MOVE

        return MoveStatus.CAN_MOVE

    def size_validation(self) -> None:
        """Validate the size.

        Raises:
            ShipSizeError: if the ship size invalid
        """
        size_dict = {
            GameObjectType.BIG_SHIP: BIG_SHIP_SIZE,
            GameObjectType.SMALL_SHIP: SMALL_SHIP_SIZE
        }
        for ship_type, excepted_size in size_dict.items():
            if (ship_type == self.type) and (excepted_size != len(self.location)):
                msg = f"The {self.type} has wrong size ->\n{
                    len(self.location)}: {self.symbol}, instead of {excepted_size}"
                raise ShipSizeError(msg)

    def location_validation(self) -> None:
        """Validate the location points are next to each other.

        Raises:
            ShipLocationError: if not all location points are next to each other
        """
        for point in self.location:
            if isinstance(point, Point) is False:
                raise ShipLocationError(
                    f"The all points location must be type of {Point.__name__} class\n -> your location = {self.location}")
        counter = 0
        all_directions = [direction for direction in Direction]
        all_directions.remove(Direction.NULL)
        for base_point in self.location:
            for other_point in self.location:
                if other_point == base_point:
                    continue
                for direction in all_directions:
                    if (base_point + direction.value) == other_point:
                        counter += 1
        if (counter // 2) < (len(self.location) - 1):
            raise ShipLocationError(
                f"The {self.symbol} -> not all locations are next to each other")
