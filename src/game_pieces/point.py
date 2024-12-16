"""
    File to define the Point object.
"""


from enum import Enum
from src.configuration_files import ROWS, COLS
from typing import Union


class Point:
    """Represent a point.

    Attributes:
        x (int): location in x axis
        y (int): location in y axis
    """

    def __init__(self, x: int, y: int) -> None:
        """Initializes a new instance of the Point class.

        Args:
            x (int): location in x axis
            y (int): location in y axis
        """
        self.__x = x
        self.__y = y

    @property
    def x(self) -> int:
        return self.__x

    @x.setter
    def x(self, value: int) -> None:
        self.__x = value

    @property
    def y(self) -> int:
        return self.__y

    @y.setter
    def y(self, value: int) -> None:
        self.__y = value

    def __copy__(self) -> "Point":
        """Copy the self point.

        Returns:
            Point: copied point
        """
        copy_point = Point(self.__x, self.__y)
        return copy_point

    def __add__(self, other: Union[int, "Point"]) -> "Point":
        """Add point to point.

        Args:
            other (Union[int, Point]): other point to add

        Returns:
            Point: the point after added
        """
        if isinstance(other, int):
            x = (self.__x + other) % ROWS
            y = (self.__y + other) % COLS
        else:
            x = (self.__x + other.x) % ROWS
            y = (self.__y + other.y) % COLS
        return Point(x, y)

    def __mul__(self, amount: int) -> "Point":
        """Multiply the Point object by scalar.

        Args:
            amount (int): scalar to multiply

        Returns:
            Point: The point after multiplied
        """
        x = self.__x * amount
        y = self.__y * amount
        return Point(x, y)

    def __eq__(self, other: "Point") -> bool:
        """Check if self points is equal to other.

        Args:
            other (Point): other point to check

        Returns:
            bool: True - if are equal, else False
        """
        return (self.__x == other.x) and (self.__y == other.y)

    def __hash__(self) -> int:
        """Get the hash value of point.

        Returns:
            int: hash value for point
        """
        return hash((self.x, self.y))

    def __str__(self) -> str:
        """Get point description.

        Returns:
            str: point description
        """
        ret_str = f"x={self.__x},y={self.__y}"
        return ret_str

    def __repr__(self) -> str:
        """Get point representation.

        Returns:
            str: point representation
        """
        return self.__str__()


class Direction(Enum):
    """Enum that represent direction of game object.
        each direction is the point with the correct base value
        in right direction.
    """
    NULL = Point(x=0, y=0)
    UP = Point(x=-1, y=0)
    DOWN = Point(x=1, y=0)
    RIGHT = Point(x=0, y=1)
    LEFT = Point(x=0, y=-1)
