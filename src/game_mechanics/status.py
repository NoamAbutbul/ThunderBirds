"""
    File to define Status to flow of the game.
"""


from enum import Enum


class Status(Enum):
    """Enum that represent status in the game. """
    NULL = 'null'
    NEW_GAME = 'new game'
    RULES = 'rules'
    RECORDS = 'records'
    RESUME = 'resume'
    PAUSE = 'pause'
    PLAY_RECORD = 'play record'
    EXIT = 'exit'
