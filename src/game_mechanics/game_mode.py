"""
    File to define available game modes
"""


from enum import Enum


class GameMode(Enum):
    """Enum that represent game modes available in the game. """
    NULL = 'null'
    PLAY = 'play mode'
    WATCH = 'watch mode'
