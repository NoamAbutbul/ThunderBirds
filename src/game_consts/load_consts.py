"""
    File to load the yaml consts file to the project.
"""


import yaml


CONSTS_YAML_PATH = r"src/game_consts/consts.yaml"


with open(CONSTS_YAML_PATH, 'r') as file:
    consts = yaml.safe_load(file)


GAME_NAME: str = consts['GAME_NAME']
LEVEL_FILE_EXTENSION: str = consts['LEVEL_FILE_EXTENSION']
RECORD_FILE_EXTENSION: str = consts['RECORD_FILE_EXTENSION']
LEVELS_DIR_PATH: str = consts['LEVELS_DIR_PATH']
RECORDS_DIR_PATH: str = consts['RECORDS_DIR_PATH']
SHORT_SLEEP: float = consts['SHORT_SLEEP']
LONG_SLEEP: float = consts['LONG_SLEEP']
BIG_SHIP_SIZE: int = consts['BIG_SHIP_SIZE']
SMALL_SHIP_SIZE: int = consts['SMALL_SHIP_SIZE']
PORTAL_SIZE: int = consts['PORTAL_SIZE']
ALL_COLORS: list[str] = consts['ALL_COLORS']
RULES: str = consts['RULES']
FPS: int = consts['FPS']
HEARTS: int = consts['HEARTS']
TIME: int = consts['TIME']
GAME_SPEED: dict[float] = consts['GAME_SPEED']
SPEED_STEPS: int = consts['SPEED_STEPS']
MAX_RECORDS_FILES: int = consts['MAX_RECORDS_FILES']
