"""
    File to define the Game class.
"""


import time
from typing import Any, Callable
from src.game_consts import FPS, LONG_SLEEP, GAME_SPEED
from src import deps
from src.game_mechanics.game_mode import GameMode
from src.game_mechanics.record import RecorderInterface
from src.game_mechanics.timer import Timer
from src.game_mechanics.status import Status
from src.game_mechanics.life_manager import LifeManager
from src.game_mechanics.level import LevelLoaderInterface
from src.game_mechanics.level import TxtLevelLoader
from src.game_mechanics.state import State, MoveStatus
