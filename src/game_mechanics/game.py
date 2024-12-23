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
from src.io import IOManager
from src.game_pieces import GameObject, GameObjectType, Direction
from src.logger import logger


class Game:
    """Represent a game.

    Attributes:
        mode (GameMode): game mode
        io_manager (IOManger): IOManager of the game
        state (State): state of the game
        timer (Timer): timer of the game
        life_manager (LifeManager): life manager of the game
        level_loader (LevelLoaderInterface): level loader of the game
        current_direction (Direction): direction input from the user
        prev_direction (Direction): previous direction input from the user
        is_paused (bool): flag to notice game paused
        is_first_frame (bool): flag to notice first game frame
        victory_count (int): count times ship victory
        is_victory (bool): flag to notice victory
        hook (Callable): hook for handle user input
        recorder (RecorderInterface): recorder of the game
        is_first_game (bool): flag to notice first game
        dt (float): time difference between the current and previous frame
        speed (list[int]): list of one item, the speed time of game
    """

    FRAME_TIME = 1 / FPS
    COOLDOWN_TIME = 3

    def __init__(self, io_manager: IOManager) -> None:
        """Initializes a new instance of the Game class.

        Args:
            io_manager (IOManager): IO manager of the game
        """
        self.__mode: GameMode = GameMode.NULL
        self.__io_manager: IOManager = io_manager
        self.__state: State = None
        self.__timer: Timer = None
        self.__life_manager: LifeManager = None
        self.__level_loader: LevelLoaderInterface = deps.get_level_loader()
        self.__current_direction: Direction = Direction.NULL
        self.__prev_direction: Direction = Direction.NULL
        self.__is_paused: bool = False
        self.__is_first_frame: bool = False
        self.__victory_count: int = 0
        self.__break_game_loop: bool = False
        self.__is_victory: bool = False
        self.__hook: Callable = None
        self.__recorder: RecorderInterface = None
        self.__dt: float = 0
        self.__speed: list[int] = [GAME_SPEED["DEFAULT_SPEED"]]

    @property
    def io_manager(self) -> IOManager:
        return self.__io_manager

    @property
    def state(self) -> State:
        return self.__state

    @property
    def timer(self) -> Timer:
        return self.__timer

    @property
    def life_manager(self) -> LifeManager:
        return self.__life_manager

    @property
    def level_loader(self) -> TxtLevelLoader:
        return self.__level_loader

    def init_new_game(self, mode: GameMode, total_time: int, hearts: int, source: Any = None) -> None:
        """Initializes a new game session.

        Args:
            mode (GameMode): game mode
            total_time (int): total time for the game
            hearts (int): hearts for the game
            source (Any, optional): source game data. Defaults to None.
        """
        logger.info(f"init the game in {mode.value}")
        self.__mode = mode
        self.io_manager.set_mode(mode, source, self.__speed)
        self.__state = State()
        self.io_manager.show_menubar()
        self.io_manager.show_bottombar()
        self.__timer = Timer(total_time)
        self.io_manager.update_menubar_time(total_time)
        self.__life_manager = LifeManager(hearts)
        self.io_manager.update_menubar_hearts(self.life_manager.current_lifes)
        self.__is_paused = False
        self.__is_first_frame = False
        self.__victory_count = 0
        self.__break_game_loop = False
        self.__current_direction = Direction.NULL
        self.__prev_direction = Direction.NULL
        self.__is_victory = False
        self.__dt = 0

    def start_with_blank_board(self) -> None:
        """Start game with a blank board. """
        self.state.init_blank_board()

    def load_level(self, filename="") -> None:
        """Load matrix level from filename

        Args:
            filename (str, optional): level filename. Defaults to "".
        """
        if filename == "":
            matrix_level = self.level_loader.load_current_level()
        else:
            matrix_level = self.level_loader.load_level_by_name(filename)
        self.state.load_board(matrix_level)

    def start(self) -> None:
        """Start the game. """
        self.state.init_new_game()
        self.io_manager.show_menubar()
        self.io_manager.show_bottombar()
        self.io_manager.set_current_player(self.state.current_player.symbol)
        self.io_manager.print_board(self.state.board)
        self.timer.start(self.io_manager.update_menubar_time)
        self.start_listen_input()
        self.activate_game_mechanism()

    def activate_game_mechanism(self) -> None:
        """Activate game mechanism.
            This function will run the game loop until one of the following conditions is met:
            - The game is paused
            - The timer has run out
            - The game loop break condition is met
        """
        if (self.__mode == GameMode.PLAY):
            self.__recorder = deps.get_record_manager(
                self.io_manager.input_manager,
                self.io_manager.output_manager,
                self.level_loader.get_current_level_filename(),
                self.timer.total_time,
                self.life_manager.started_lifes)
            self.__recorder.start_record()

        while (not self.__is_paused) and (not self.timer.is_time_over()) and (not self.__break_game_loop):
            self.game_loop()
            if self.__is_paused and (not self.timer.is_time_over()):
                self.activate_pause_menu()

        if not self.__is_paused:
            if self.__is_victory:
                self.timer.make_time_over()
                self.__break_game_loop = True
                return

            if self.life_manager.current_lifes >= 1:
                self.handle_reduce_life_case()
                return

            elif self.timer.is_time_over():
                time.sleep(LONG_SLEEP)
                self.io_manager.update_menubar_msg("Time Over")
                self.__break_game_loop = True
                return

            else:
                time.sleep(LONG_SLEEP)
                self.__break_game_loop = True

    def game_loop(self) -> None:
        """The main game loop.
            This function contains the main game loop. It calculate the time difference between frames,
            updates the game state accordingly, and calls the update function.
        """
        self.show_watch_speed()
        self.__dt = Game.FRAME_TIME / self.__speed[0]
        current_time = time.time()
        accumulator = 0.0
        while (not self.timer.is_time_over()) and (not self.__is_paused) and (not self.__break_game_loop) and (not self.life_manager.is_reduced_life_in_this_frame):
            self.show_watch_speed()
            self.__dt = Game.FRAME_TIME / self.__speed[0]
            new_time = time.time()
            frame_time = new_time - current_time
            current_time = new_time
            accumulator += frame_time
            while accumulator >= self.__dt:
                self.game_loop_iteration()
                accumulator -= self.__dt
            sleep_time = self.__dt - (time.time() - current_time) - accumulator
            if sleep_time > 0:
                time.sleep(sleep_time)

    def show_watch_speed(self) -> None:
        """Show watch speed to user if dt was changed. """
        if self.__mode == GameMode.WATCH:
            if (Game.FRAME_TIME / self.__speed[0]) != self.__dt:
                self.io_manager.update_menubar_msg(
                    f"speed watch: {self.__speed[0]}")

    def game_loop_iteration(self) -> None:
        """Game loop iteration.
            Here is all actions that happened in an iteration of the game loop.
        """
        self.apply_move()
        if (self.__prev_direction == self.__current_direction) and (not self.__is_first_frame):
            self.update_player_movement(
                self.state.current_player, self.__current_direction)
            self.apply_move()
        self.apply_gravity()

    def handle_key_input(self, key: str) -> None:
        """Handle key input from the user.

        Args:
            key (str): the key that triggered
        """
        if self.__is_paused:
            return

        logger.debug(f"input game handle for {key}")
        buttons = self.io_manager.get_buttons()
        key_direction = {
            buttons.RIGHT.value: Direction.RIGHT,
            buttons.LEFT.value: Direction.LEFT,
            buttons.UP.value: Direction.UP,
            buttons.DOWN.value: Direction.DOWN
        }
        more_than_one_ship = (self.state.ships_amount -
                              self.__victory_count) > 1
        if key == buttons.EXIT.value:
            self.handle_pause_action()

        elif (key == buttons.SHIP_SWITCH.value) and (more_than_one_ship):
            self.handle_switch_player_action()

        elif key in key_direction:
            self.handle_change_player_direction(key_direction[key])

    def handle_pause_action(self) -> None:
        """Handle pause action from the user input. """
        if self.__is_paused:
            self.resume()
        else:
            self.pause()

    def handle_switch_player_action(self) -> None:
        """Handle switch player action from the user input. """
        self.__prev_direction = Direction.NULL
        self.state.switch_current_player()
        self.io_manager.set_current_player(self.state.current_player.symbol)

    def handle_change_player_direction(self, direction: Direction) -> None:
        """Handle change player direction from the user input.

        Args:
            direction (Direction): new direction to player
        """
        self.__current_direction = direction
        self.__prev_direction = self.__current_direction

    def update_player_movement(self, game_object: GameObject, direction: Direction) -> None:
        """Update player movement (if legally) on the board.

        Args:
            game_object (GameObject): game object wants to move
            direction (Direction): move direction
        """
        if direction == Direction.NULL:
            return
        need_to_move: list[GameObject] = []
        move_status = self.state.can_move(
            game_object, [game_object.mass], game_object, direction, need_to_move)
        if move_status == MoveStatus.REDUCE_LIFE:
            if not self.life_manager.is_reduced_life_in_this_frame:
                self.handle_reduce_life_case()
        elif move_status == MoveStatus.CAN_MOVE:
            self.handle_move_case(need_to_move, direction)
        elif move_status == MoveStatus.VICTORY:
            self.handle_victory()

    def handle_victory(self, game_object: GameObject) -> None:
        """Handle for victory case to game_object

        Args:
            game_object (GameObject): game_object that won
        """
        self.__victory_count += 1
        self.handle_switch_player_action()
        if self.__mode == GameMode.PLAY:
            self.__recorder.save_prev_key_to_record()
        dest = []
        self.state.move_game_object(
            game_object.symbol, game_object.location, dest)
        self.io_manager.move_item(
            game_object.symbol, game_object.location, dest)
        game_object.location = []
        self.state.objects.remove(game_object)
        if self.__victory_count == self.state.ships_amount:
            self.stop_listen_input()
            self.__is_victory = True
            self.io_manager.show_victory_message()
            self.__break_game_loop = True
            self.timer.make_time_over()
            if self.__mode == GameMode.PLAY:
                self.__recorder.save_record()
                self.__recorder.reset_record_file()
                self.go_to_next_level()

    def handle_reduce_life_case(self) -> None:
        """Handle for reduce life case. """
        if self.life_manager.is_reduced_life_in_this_frame:
            return
        self.stop_listen_input()
        self.life_manager.is_reduced_life_in_this_frame = True
        self.__current_direction = Direction.NULL
        self.life_manager.reduce_life()
        self.io_manager.update_menubar_hearts(self.life_manager.current_lifes)
        self.io_manager.show_reduce_life_message()
        if self.life_manager.is_over():
            self.timer.make_time_over()
            self.io_manager.show_lose_message()
            self.__break_game_loop = True
            return
        if self.__mode == GameMode.PLAY:
            self.reset_level()
        else:
            self.end_game()

    def handle_move_case(self, need_to_move: list[GameObject], direction: Direction) -> None:
        """Handle for move case.

        Args:
            need_to_move (list[GameObject]): game objects that need to move
            direction (Direction): direction of the move
        """
        for game_object in need_to_move:
            self.state.move_game_object_to_first(game_object)
            game_object.direction = direction

    def apply_move(self) -> None:
        """Apply move action for all game objects in the game. """
        for obj in self.state.objects:
            self.move_game_object(obj)

    def move_game_object(self, game_object: GameObject) -> None:
        """Move game object in the logic board and in the view.

        Args:
            game_object (GameObject): game object to move
        """
        if game_object.direction != Direction.NULL:
            symbol = game_object.symbol
            source = game_object.copied_location
            game_object.move(game_object.direction)
            dest = game_object.location
            self.state.move_game_object(symbol, source, dest)
            self.io_manager.move_item(symbol, source, dest)
            game_object.direction = Direction.NULL

    def apply_gravity(self) -> None:
        """Apply gravity for all blocks objects. """
        for game_object in self.state.objects:
            if game_object.type in [GameObjectType.BLOCK_LETTERS, GameObjectType.BLOCK_NUMBERS]:
                if (game_object.direction == Direction.NULL):
                    self.update_player_movement(game_object, Direction.DOWN)

    def pause(self) -> None:
        """Pause the game. """
        logger.info("Game Paused")
        self.timer.pause()
        self.stop_listen_input()
        if self.__mode == GameMode.PLAY:
            self.__recorder.stop_record()
        self.__is_paused = True

    def activate_pause_menu(self) -> None:
        """Activate the pause menu
            and map functions by user input status.
        """
        status = self.io_manager.activate_pause_menu()
        status_action = {
            Status.RESUME: self.resume,
            Status.EXIT: self.end_game
        }
        if status in status_action:
            status_action[status]()

    def resume(self) -> None:
        """Resume the game. """
        logger.info("Game Resuming")
        self.timer.resume()
        self.__is_paused = False
        self.io_manager.clear_output()
        self.io_manager.show_menubar()
        self.io_manager.print_board(self.state.board)
        self.io_manager.show_bottombar()
        self.io_manager.set_current_player(self.state.current_player.symbol)
        self.start_listen_input()
        if self.__mode == GameMode.PLAY:
            self.__recorder.start_record()

    def reset_level(self) -> None:
        """Start over the level. """
        sec_time = 0
        self.timer.make_time_over()
        while sec_time < Game.COOLDOWN_TIME:
            self.io_manager.update_menubar_msg(
                f"New game start in {Game.COOLDOWN_TIME - sec_time} seconds...")
            time.sleep(LONG_SLEEP)
            sec_time += 1
        self.init_new_game(self.__mode, self.timer.started_time,
                           self.life_manager.current_lifes)
        self.load_level()
        self.io_manager.update_menubar_msg("The level start over")
        self.start()

    def go_to_next_level(self) -> None:
        """Go to the next level.
            Reset time & lifes and start next level.
        """
        if not self.level_loader.is_next_level_exist():
            self.io_manager.update_menubar_msg(
                f"Congratulation!!!, you passed all the levels")
            time.sleep(LONG_SLEEP)
            return

        sec_time = 0
        self.timer.make_time_over()
        while sec_time < Game.COOLDOWN_TIME:
            self.io_manager.update_menubar_msg(
                f"Next level will start in {Game.COOLDOWN_TIME - sec_time} seconds...")
            time.sleep(LONG_SLEEP)
            sec_time += 1

        self.init_new_game(self.__mode, self.timer.started_time,
                           self.life_manager.started_lifes)
        matrix_level = self.level_loader.load_next_level()
        self.state.load_board(matrix_level)
        self.io_manager.update_menubar_msg("The next level start")
        self.start()

    def end_game(self) -> None:
        """End the game. """
        self.__break_game_loop = True
        self.stop_listen_input()
        if self.__mode == GameMode.PLAY:
            self.__recorder.stop_record()
        self.timer.make_time_over()
        self.io_manager.clear_output()

    def start_listen_input(self) -> None:
        """Start listen to game input. """
        self.__hook = self.io_manager.start_listening(self.handle_key_input)

    def stop_listen_input(self) -> None:
        """Stop listen to game input. """
        self.io_manager.stop_listening(self.__hook)
        self.__hook = None
