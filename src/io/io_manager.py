"""
    File to define the IOManager class.
"""


import time
from typing import Any, Callable
from src import deps
from src.game_mechanics.game_mode import GameMode
from src.game_mechanics.status import Status
from src.io.input import InputInterface
from src.io.output import OutputInterface
