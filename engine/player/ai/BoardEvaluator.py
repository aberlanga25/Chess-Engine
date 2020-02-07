from abc import ABC, abstractmethod

from engine.board import Board


class BoardEvaluator(ABC):

    @abstractmethod
    def evaluate(self, board: Board.Board, depth: int) -> int:
        pass