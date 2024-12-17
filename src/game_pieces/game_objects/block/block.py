"""
    File to define the Block game object.
"""


from src.game_pieces.point import Point, Direction
from src.game_pieces.game_object import GameObject, GameObjectType, MoveStatus


class Block(GameObject):
    """Represent a block object (inherits from GameObject)

    Attributes:
        location (list[Point]): location in the board
        symbol (str): symbol of the object
        mass (int): mass of the object
        direction (Direction): direction of the object
        kind (BlockKind): kind of the block
    """

    def __init__(self, location: list[Point] = None, symbol: str = None, mass: int = 0, direction: Direction = Direction.NULL) -> None:
        """Initializes a new instance of the Block class.

        Args:
            location (list[Point], optional): location in the board. Defaults to None.
            symbol (str, optional): symbol of the object. Defaults to None.
            mass (int, optional): mass of the object. Defaults to 0.
            direction (Direction, optional): direction of the object. Defaults to Direction.NULL.
        """
        super().__init__(location, symbol, 0, direction)

    def __str__(self) -> str:
        """Get block object description.

        Returns:
            str: block object description
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
        if root_pusher.type not in [GameObjectType.BLOCK_LETTERS, GameObjectType.BLOCK_NUMBERS]:
            if not self.is_my_pusher(root_pusher):
                return MoveStatus.CANNOT_MOVE

        if root_pusher.type in [GameObjectType.BIG_SHIP, GameObjectType.SMALL_SHIP]:
            if power[0] < self.mass:
                return MoveStatus.CANNOT_MOVE
            else:
                power[0] -= self.mass

        if root_pusher.type in [GameObjectType.BLOCK_LETTERS, GameObjectType.BLOCK_NUMBERS]:
            if direction == Direction.DOWN:
                power[0] += self.mass

        return MoveStatus.CAN_MOVE

    def is_my_pusher(self, pusher: GameObject) -> bool:
        """Checking if pusher can push me.

        Args:
            pusher (GameObject): pusher game object 

        Returns:
            bool: True - if this game object cab push me, else False
        """
        if self.type == GameObjectType.BLOCK_LETTERS:
            if pusher.type == GameObjectType.BIG_SHIP:
                return True
            return False
        elif self.type == GameObjectType.BLOCK_NUMBERS:
            if pusher.type == GameObjectType.SMALL_SHIP:
                return True
        return False
