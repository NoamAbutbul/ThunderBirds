"""
    File to define the RecordInterface of the game.
"""


from abc import ABC, abstractmethod


class RecordInterface(ABC):
    """Define base recorder interface to the game. """

    @abstractmethod
    def start_record(self) -> None:
        """Start recording the game. """
        raise NotImplementedError

    @abstractmethod
    def stop_record(self) -> None:
        """Stop recording the game. """
        raise NotImplementedError

    @abstractmethod
    def save_record(self) -> None:
        """Save the record file. """
        raise NotImplementedError

    @abstractmethod
    def save_prev_key_to_record(self) -> None:
        """Save the previous key to the record file. """
        raise NotImplementedError

    @abstractmethod
    def reset_record_file(self) -> None:
        """Reset the record file. """
        raise NotImplementedError
