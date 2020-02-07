from abc import ABC, abstractmethod
from engine.board import Board
from engine.board import Move


class MoveStrategy(ABC):

    @abstractmethod
    def execute(self, board: Board.Board, depth: int) -> Move.Move:
        pass
