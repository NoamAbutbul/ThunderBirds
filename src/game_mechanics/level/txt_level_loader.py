"""
    File to define TxtLevelLoader.
"""


import os
import glob
from src.game_consts import LEVELS_DIR_PATH, LEVEL_FILE_EXTENSION
from src.configuration_files import ROWS, COLS
from src.game_pieces.symbols import LogicSymbol
from src.game_mechanics.level.level_loader_interface import LevelLoaderInterface
from src.game_mechanics.level.level_loader_exception import LevelPathError, LevelSizeError, LevelSymbolsError, LevelElementsError
from src.logger import logger


class TxtLevelLoader(LevelLoaderInterface):
    """A class for loading levels from a .txt file.

    Attributes:
        current_level (int): current index level file
    """

    LEVEL_FILES = sorted(
        glob.glob(os.path.join(LEVELS_DIR_PATH, '*.level.txt')))

    def __init__(self) -> None:
        """Initializes a new instance of the TxtLevelLoader class. """
        self.__current_level: int = 0
        logger.debug(f"my LEVEL_FILES = {TxtLevelLoader.LEVEL_FILES}")

    def load_level_by_path(self, level_path: str) -> list[list[str]]:
        """Load level board by path.

        Args:
            level_path (str): level path

        Returns:
            list[list[str]]: board that loaded
        """
        self.path_validation(level_path)
        with open(level_path, 'r') as file:
            level_matrix = [list(line.rstrip('\n') for line in file)]
        self.level_board_validation(level_matrix)
        return level_matrix

    def path_validation(self, path: str) -> None:
        """Validate level path.

        Args:
            path (str): path to valid

        Raises:
            LevelPathError: if level path is invalid
        """
        if path == None:
            raise LevelPathError(f"The level path to load is None")
        if not os.path.isfile(path):
            raise LevelPathError(f"level file: '{path}' does not exist")
        if LEVEL_FILE_EXTENSION not in path:
            raise LevelPathError(
                f"The file {path} does not with {LEVEL_FILE_EXTENSION}")

    def level_board_validation(self, level_board: list[list[str]]) -> None:
        """Validate level board.

        Args:
            level_board (list[list[str]]): level board to validate
        """
        self.board_size_validate(level_board)
        self.board_symbols_validate(level_board)
        self.board_elements_validate(level_board)

    def board_size_validate(self, board: list[list[str]]) -> None:
        """Validate the size of the level board.

        Args:
            board (list[list[str]]): the level board to validate

        Raises:
            LevelSizeError: if the board size in invalid
        """
        if (len(board) != ROWS):
            raise LevelSizeError(
                f"The level has wrong number of rows\nHas {len(board)}, instead of {ROWS}")
        for row in range(ROWS):
            if len(board[row] != COLS):
                raise LevelSizeError(
                    f"The level has wrong number of cols -> In line {row+1}, Has {len(board[row])}, instead of {COLS}")

    def board_symbols_validate(self, board: list[list[str]]) -> None:
        """Validate the symbols in the level board.

        Args:
            board (list[list[str]]): the level board to validate

        Raises:
            LevelSymbolsError: if the board contain invalid symbols
        """
        symbols = LogicSymbol.all_values()
        for row in range(ROWS):
            for col in range(COLS):
                if board[row][col] not in symbols:
                    raise LevelSymbolsError(
                        f"The level contain wrong symbols ->\nrow = {row}, col = {col}, possible symbols = {symbols}")

    def board_elements_validate(self, board: list[list[str]]) -> None:
        """Validate elements in the level board.

        Args:
            board (list[list[str]]): the level board to validate

        Raises:
            LevelElementsError: if the level board elements is invalid
        """
        counters = {
            LogicSymbol.BIG_SHIP.value: 0,
            LogicSymbol.SMALL_SHIP.value: 0,
            LogicSymbol.PORTAL.value: 0
        }
        for row in range(ROWS):
            for col in range(COLS):
                if board[row][col] in counters:
                    counters[board[row][col]] += 1

        if counters[LogicSymbol.BIG_SHIP.value] == 0:
            raise LevelElementsError(
                f"The level does not contain a {LogicSymbol.BIG_SHIP.value}: Big Ship")

        if counters[LogicSymbol.SMALL_SHIP.value] == 0:
            raise LevelElementsError(
                f"The level does not contain a {LogicSymbol.SMALL_SHIP.value}: Small Ship")

        if counters[LogicSymbol.PORTAL.value] == 0:
            raise LevelElementsError(
                f"The level does not contain a {LogicSymbol.PORTAL.value}: Portal")

    def load_current_level(self) -> list[list[str]]:
        """Load the current level.

        Returns:
            list[list[str]]: the current level matrix
        """
        level_matrix = None
        current_level_path = ""
        if self.__current_level < len(TxtLevelLoader.LEVEL_FILES):
            current_level_path = TxtLevelLoader.LEVEL_FILES[self.__current_level]
        level_matrix = self.load_level_by_path(current_level_path)
        return level_matrix

    def load_level_by_name(self, filename: str) -> list[list[str]]:
        """Load a level by its name.

        Args:
            filename (str): the name of the level file

        Returns:
            list[list[str]]: the level matrix
        """
        current_level_path = os.path.join(LEVELS_DIR_PATH, filename)
        level_matrix = self.load_level_by_path(current_level_path)
        return level_matrix

    def load_next_level(self) -> list[list[str]]:
        """Load the next level.

        Returns:
            list[list[str]]: the next level matrix
        """
        self.__current_level += 1
        level_matrix = self.load_current_level()
        return level_matrix

    def get_current_level_filename(self) -> str:
        """Get current level filename.

        Returns:
            str: current level filename
        """
        current_level_filename = ""
        if self.__current_level < len(TxtLevelLoader.LEVEL_FILES):
            current_level_path = TxtLevelLoader.LEVEL_FILES[self.__current_level]
            current_level_filename = os.path.basename(current_level_path)
        return current_level_filename

    def is_next_level_exist(self) -> bool:
        """Check if there is next level.

        Returns:
            bool: True - if next level exist, else False
        """
        next_level_exist = False
        if (self.__current_level + 1) < len(TxtLevelLoader.LEVEL_FILES):
            next_level_exist = True
        return next_level_exist
