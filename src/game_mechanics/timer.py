"""
    File to define the Timer of the game.
"""


import time
from threading import Thread
from typing import Callable
from src.game_consts import SHORT_SLEEP


class Timer:
    """Represent a timer.

    Attributes:
        started_time (int): started time of the game
        total_time (int): total time of the game
        time_counter (int): time counter of the game
        timer_thread (Thread): timer thread of the game
        is_paused (bool): flag to notice timer paused
        is_over (bool): flag to notice time over
    """

    def __init__(self, total_time: int) -> None:
        """Initializes a new instance of the Game class.

        Args:
            total_time (int): total time of the game
        """
        self.__started_time: int = total_time
        self.__total_time: int = total_time
        self.__time_counter: int = 0
        self.__timer_thread: Thread = None
        self.__is_paused: bool = False
        self.__is_over: bool = False

    @property
    def started_time(self) -> int:
        return self.__started_time

    @property
    def time_counter(self) -> int:
        return self.__time_counter

    @property
    def total_time(self) -> int:
        return self.__total_time

    def start(self, update_output_time: Callable) -> None:
        """Starting the timer for the game.

        Args:
            update_output_time (Callable): function to update output time
        """
        self.__timer_thread = Thread(
            target=self.__count_down, args=(update_output_time,))
        self.__timer_thread.setName("count down timer")
        if self.__total_time != 0:
            self.__timer_thread.start()

    def make_time_over(self) -> None:
        """Making time over for the count down timer. """
        self.__is_over = True
        self.__total_time = 0
        time.sleep(SHORT_SLEEP)

    def __count_down(self, update_output_time: Callable) -> None:
        """Count down timer and activate update_output_time function 
            with the remaining time

        Args:
            update_output_time (Callable): function to update output time
        """
        while (self.__time_counter < self.__total_time) and (not self.__is_over):
            if not self.__is_paused:
                self.__time_counter += 1
                remaining_time = self.__total_time - self.__time_counter
                update_action_time = update_action_time(remaining_time)
                if update_action_time < 1:
                    time.sleep(1 - update_action_time)
            if self.__is_paused:
                pass
        self.make_time_over()

    def pause(self) -> None:
        """Pause the timer. """
        self.__is_paused = True

    def resume(self) -> None:
        """Resume the timer. """
        self.__is_paused = False

    def is_time_over(self) -> bool:
        """Check if time over.

        Returns:
            bool: True - if time over, else False
        """
        time_over = self.__time_counter >= self.__total_time
        return time_over
