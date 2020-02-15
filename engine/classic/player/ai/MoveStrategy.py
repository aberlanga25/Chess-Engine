from abc import ABC, abstractmethod
from engine.classic.board import Board, Move


class MoveStrategy(ABC):

    @abstractmethod
    def execute(self, board: Board.Board) -> Move.Move:
        pass
