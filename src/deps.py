"""
    File to inject objects of specific hardware as general purposes objects
    when other class needed to be implemented into the general object, the change to the new class needs to be here.
"""


from typing import Any
from src.game_mechanics.game_mode import GameMode
from src.io.output import OutputInterface, CMDManager
from src.io.input import InputInterface, KeyboardInput, FileInput
from src.game_mechanics.level import LevelLoaderInterface, TxtLevelLoader
from src.game_mechanics.record import RecorderInterface, RecorderTxt


def get_output_manager() -> OutputInterface:
    """Get output manager object.

    Returns:
        OutputInterface: output manager object
    """
    return CMDManager()


def get_input_manager(mode: GameMode, source: Any, speed: list[float]) -> InputInterface:
    """Get input manager object.

    Args:
        mode (GameMode): game mode
        source (Any): source data
        speed (list[float]): list with one item, speed of the game frame

    Returns:
        InputInterface: input manager object
    """
    input_manager = None
    mode_input_manager = {
        GameMode.PLAY: KeyboardInput,
        GameMode.WATCH: FileInput
    }
    if mode in mode_input_manager:
        input_manager = mode_input_manager[mode](source, speed)
    return input_manager


def get_level_loader() -> LevelLoaderInterface:
    """Get level loader object.

    Returns:
        LevelLoaderInterface: level loader object
    """
    return TxtLevelLoader()


def get_record_manager(input_manager: InputInterface, output_manager: OutputInterface, level_filename: str, time_for_game: int, hearts_for_game: int) -> RecorderInterface:
    """Get recorder object.

    Args:
        input_manager (InputInterface): input manager for the game
        output_manager (OutputInterface): output manager for the game
        level_filename (str): filename of the level
        time_for_game (int): time for the game
        hearts_for_game (int): hearts for the game

    Returns:
        RecorderInterface: recorder object
    """
    return RecorderTxt(input_manager, output_manager, level_filename, time_for_game, hearts_for_game)
