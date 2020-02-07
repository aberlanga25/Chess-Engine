from engine.player.ai.BoardEvaluator import BoardEvaluator
from engine.board import Board
from engine.player import Player

from typing import *


class StandardBoardEvaluator(BoardEvaluator):

    def evaluate(self, board: Board.Board, depth: int) -> int:

        return self.scorePlayer(board, board.whitePlayer, depth) - self.scorePlayer(board, board.whitePlayer, depth)

    def scorePlayer(self, board: Board.Board, player: Player.Player, depth: int) -> int:

        return self.pieceValue(player)

    def mobility(self, player: Player.Player) -> int:
        return len(player.legalMoves)

    @staticmethod
    def pieceValue(player: Player.Player) -> int:
        pieceValueScore = 0
        for piece in player.activePieces:
            pieceValueScore += piece.pieceType.pieceValue()
        return pieceValueScore
