"""
    File to define the basic GameObject
"""


from enum import Enum
from abc import ABC, abstractmethod
from typing import Union
from src.game_pieces import Point, Direction
from src.game_pieces import GameObjectType
from src.configuration_files import ROWS, COLS
from src.logger import logger


class MoveStatus(Enum):
    """Enum that represent move status. """
    CANNOT_MOVE = -1
    CAN_MOVE = 0
    REDUCE_LIFE = 1
    VICTORY = 100


class GameObject(ABC):
    """Represent a game object (abstract class).

    Attributes:
        location (list[Point]): location in the board
        symbol (str): symbol of the object
        mass (int): mass of the object
        direction (Direction): direction of the object
        type (GameObjectType): game object type
    """

    def __init__(self, location: Union[list[Point], None], symbol: str, mass: int, direction: Direction) -> None:
        """Initializes a new instance of the GameObject class.

        Args:
            location (Union[list[Point], None]): location in the board
            symbol (str): symbol of the object
            mass (int): mass of the object
            direction (Direction): direction of the object
        """
        super().__init__()
        if isinstance(location, list):
            self.__location: list[Point] = location
        else:
            self.__location: list[Point] = []
        self.__symbol: str = symbol
        self.__mass: int = mass
        self.__direction: Direction = direction
        self.__type = GameObjectType.get_type_by_symbol(symbol)

    @property
    def location(self) -> list[Point]:
        copy_location = []
        for loc in self.__location:
            copy_location.append(loc)
        return copy_location

    @location.setter
    def location(self, location: list[Point]) -> None:
        self.__location = []
        for loc in location:
            self.__location.append(loc)

    @property
    def symbol(self) -> str:
        return self.__symbol

    @symbol.setter
    def symbol(self, symbol: str) -> None:
        self.__symbol = symbol

    @property
    def mass(self) -> int:
        return self.__mass

    @mass.setter
    def mass(self, mass: int) -> None:
        self.__mass = mass

    @property
    def direction(self) -> Direction:
        return self.__direction

    @direction.setter
    def direction(self, direction: Direction) -> None:
        self.__direction = direction

    @property
    def copied_location(self) -> list[Point]:
        copy_location: list[Point] = []
        for point in self.__location:
            copy_location.append(point.__copy__())
        return copy_location

    @property
    def type(self) -> GameObjectType:
        return self.__type

    def add_point(self, point: Point) -> None:
        """Add new point to game object location.

        Args:
            point (Point): point to add
        """
        self.__location.append(point)

    def move(self, direction: Direction) -> None:
        """Move the game object one step in direction.

        Args:
            direction (Direction): direction to move
        """
        logger.debug(f"old_loc = {self.location}")
        for point in self.location:
            point.x = (point.x + direction.value.x) % ROWS
            point.y = (point.y + direction.value.y) % COLS
        logger.debug(f"new_loc = {self.location}")

    @abstractmethod
    def can_be_pushed(self, root_pusher: "GameObject", power: list[int], pusher: "GameObject", direction: Direction) -> MoveStatus:
        """Checking if self can be pushed by root_pusher in some direction.

        Args:
            root_pusher (GameObject): root pusher that want to push
            power (list[int]): list with one value: current power mass
            pusher (GameObject): pusher game object
            direction (Direction): direction of pushing

        Returns:
            MoveStatus: status for that move
        """
        pass  # TODO -> Check if can raise here NotImplementedError

    def __str__(self) -> str:
        """Get game object description.

        Returns:
            str: game object description
        """
        ret_str = "\n"
        ret_str += f"location = {self.__location}\n"
        ret_str += f"symbol = {self.__symbol}\n"
        ret_str += f"mass = {self.__mass}\n"
        ret_str += f"direction = {self.__direction}\n"
        ret_str += f"type = {self.__type}\n"
        return ret_str

    def __repr__(self) -> str:
        """Get game object representation.

        Returns:
            str: game object representation
        """
        return self.__str__()
