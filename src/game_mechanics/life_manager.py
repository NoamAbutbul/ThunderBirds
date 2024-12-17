"""
    File to define the LifeManager of the game.        
"""


from src.logger import logger


class LifeManager:
    """Manage the lifes in the game.

    Attributes:
        started_lifes (int): lifes at the beginning of the game
        current_lifes (int): current lifes in the game
        is_ever_reduced_life (bool): flag to notice ever reduced life
        is_reduced_life_in_this_frame (bool): flag to notice if life reduced in this frame
    """

    def __init__(self, lifes: int) -> None:
        """Initializes a new instance of the LifeManager class.

        Args:
            lifes (int): lifes for the game
        """
        self.__started_lifes: int = lifes
        self.__current_lifes: int = lifes
        self.__is_ever_reduced_life: bool = False
        self.__is_reduced_life_in_this_frame: bool = False

    @property
    def started_lifes(self) -> int:
        return self.__started_lifes

    @property
    def current_lifes(self) -> int:
        return self.__current_lifes

    @property
    def is_ever_reduced_life(self) -> bool:
        return self.__is_ever_reduced_life

    @property
    def is_reduced_life_in_this_frame(self) -> bool:
        return self.__is_reduced_life_in_this_frame

    @is_reduced_life_in_this_frame.setter
    def is_reduced_life_in_this_frame(self, value: bool) -> None:
        self.__is_reduced_life_in_this_frame = value

    def reduce_life(self) -> None:
        """Reduces the life by 1. """
        self.__current_lifes -= 1
        self.__is_ever_reduced_life = True
        self.__is_reduced_life_in_this_frame = True
        logger.debug(f"Life reduced, current hearts = {self.__current_lifes}")

    def is_over(self) -> bool:
        """Check if the amount of lifes is over.

        Returns:
            bool: True - if amount is over, else False
        """
        is_over = False
        if self.__current_lifes == 0:
            is_over = True
        return is_over

    def __str__(self) -> str:
        """Get LifeManager description.

        Returns:
            str: LifeManager description
        """
        ret_str = f"started_lifes = {self.__started_lifes}\n"
        ret_str += f"current_lifes = {self.__current_lifes}\n"
        ret_str += f"is_ever_reduced_life = {self.__is_ever_reduced_life}\n"
        ret_str += f"is_reduced_life_in_this_frame = {self.__is_reduced_life_in_this_frame}\n"  # noqa
        return ret_str
