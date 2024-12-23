"""
    main.py file
    To run the game -> run this file.
"""


from src.game_mechanics.controller import Controller


def main() -> None:
    controller = Controller()
    controller.run_game()


if __name__ == "__main__":
    main()
