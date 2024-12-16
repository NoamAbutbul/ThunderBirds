"""
    File to load the yaml configurations file to the project.
"""


import yaml
from enum import Enum
from src.game_consts import ALL_COLORS
from src.configuration_files.configuration_exception import ConfigurationError, ColorError, BoardSizeError


CONFIGURATION_YAML_PATH = r"configuration.yaml"


try:
    with open(CONFIGURATION_YAML_PATH, 'r') as file:
        conf = yaml.safe_load(file)
except FileNotFoundError:
    raise ConfigurationError(
        f"The file {CONFIGURATION_YAML_PATH} does not exist")
except PermissionError:
    raise ConfigurationError(
        f"You do not have permission to read the file {CONFIGURATION_YAML_PATH}")
except yaml.YAMLError as e:
    raise ConfigurationError(
        f"Error during load {CONFIGURATION_YAML_PATH} file, {e}")


try:
    ROWS: int = conf['ROWS']
    COLS: int = conf['COLS']
except KeyError:
    raise BoardSizeError(
        f"The ROWS / COLS does not configured well in the {CONFIGURATION_YAML_PATH}")


def validate_colors(all_colors: list[str], cls_name: str) -> None:
    """Validate all_colors list.

    Args:
        all_colors (list[str]): all colors list
        cls_name (str): class name for message

    Raises:
        ConfigurationError: if any color does not exist in ALL_COLORS
    """
    for color in all_colors:
        if color.value not in ALL_COLORS:
            raise ColorError(
                f"The color '{color.value}' of the {cls_name} does not exits\n -> all available colors = {ALL_COLORS}")


class GameObjectColor(Enum):
    """Enum that define colors for GameObjects. """
    try:
        WALL: str = conf['WALL_SIGN_COLOR']
        BIG_SHIP: str = conf['BIG_SHIP_SIGN_COLOR']
        SMALL_SHIP: str = conf['SMALL_SHIP_SIGN_COLOR']
        BLOCK_LETTERS: str = conf['BLOCK_SIGN_LETTERS_COLOR']
        BLOCK_NUMBERS: str = conf['BLOCK_SIGN_NUMBERS_COLOR']
        # TODO -> change here to PORTAL_SIGN_COLOR as well
        PORTAL: str = conf['PORTAL_SIGN']
    except KeyError:
        raise ColorError(
            f"The Game Objects Colors does not configured well in the {CONFIGURATION_YAML_PATH}")


all_game_objects_colors = [color for color in GameObjectColor]
validate_colors(all_game_objects_colors, GameObjectColor.__name__)


class GameInformationColors(Enum):
    """Enum that define colors for game information. """
    try:
        TIME: str = conf['TIME_COLOR']
        HEARTS: str = conf['HEARTS_COLOR']
        HEADER: str = conf['HEADER_COLOR']
    except KeyError:
        raise ColorError(
            f"The Game Information Colors does not configured well in the {CONFIGURATION_YAML_PATH}")


all_game_information_colors = [color for color in GameInformationColors]
validate_colors(all_game_information_colors, GameInformationColors.__name__)


KEYBOARD_BUTTONS: dict[str] = conf['KEYBOARD_BUTTONS']
