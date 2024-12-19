"""
    File to define the Portal game object.
"""


from src.game_consts import PORTAL_SIZE
from src.game_pieces.point import Point, Direction
from src.game_pieces.game_object import GameObject, GameObjectType, MoveStatus
from src.game_pieces.game_objects.portal.portal_exception import PortalSizeError


class Portal(GameObject):
    """Represent a portal object (inherits from GameObject).

    Attributes:
        location (list[Point]): location in the board
        symbol (str): symbol of the object
        mass (int): mass of the object
        direction (Direction): direction of the object
        type (GameObjectType): game object type
    """

    def __init__(self, location: list[Point] = None, symbol: str = None, mass: int = 0, direction: Direction = Direction.NULL) -> None:
        """Initializes a new instance of the Portal class.

        Args:
            location (list[Point], optional): location in the board. Defaults to None.
            symbol (str, optional): symbol of the object. Defaults to None.
            mass (int, optional): mass of the object. Defaults to 0.
            direction (Direction, optional): direction of the object. Defaults to Direction.NULL.
        """
        super().__init__(location, symbol, 0, direction)
        self.size_validation()

    def __str__(self) -> str:
        """Get portal object description.

        Returns:
            str: portal object description
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
        if pusher.type in [GameObjectType.BIG_SHIP, GameObjectType.SMALL_SHIP]:
            return MoveStatus.VICTORY
        return MoveStatus.CANNOT_MOVE

    def size_validation(self) -> None:
        """Validate portal size.

        Raises:
            PortalSizeError: if the portal size wrong
        """
        if len(self.location) != PORTAL_SIZE:
            msg = f"The {self.symbol} has wrong size ->\n{len(self.location)}, instead of {PORTAL_SIZE}"  # noqa
            raise PortalSizeError(msg)
