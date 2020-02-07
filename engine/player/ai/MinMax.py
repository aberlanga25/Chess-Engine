from engine.player.ai.MoveStrategy import MoveStrategy
from engine.player.ai.StandardBoardEvaluator import StandardBoardEvaluator
from engine.board import Board
from engine.board import Move, MoveTransition

from typing import *
from time import time


class MinMax(MoveStrategy):

    def __init__(self):
        self.boardEvaluator = StandardBoardEvaluator()

    def __str__(self):
        return "MiniMax"

    def execute(self, board: Board.Board, depth: int) -> Move.Move:
        startTime: float = time()
        bestMove: Move.Move = None
        highestSeenValue = float('-inf')
        lowestSeenValue = float('inf')

        print(board.currentPlayer + "Thinking with Depth = " + depth)

        numMoves = len(board.currentPlayer.legalMoves)

        for move in board.currentPlayer.legalMoves:
            moveTransition = board.currentPlayer.makeMove(move)
            if moveTransition.moveStatus.isDone():
                currentValue = self.min(moveTransition.transitionBoard, depth-1) if board.currentPlayer.alliance().isWhite() \
                    else self.max(moveTransition.transitionBoard, depth-1)
                if board.currentPlayer.alliance().isWhite() and currentValue >= highestSeenValue:
                    highestSeenValue = currentValue
                    bestMove = move
                elif board.currentPlayer.alliance().isBlack() and currentValue <= lowestSeenValue:
                    lowestSeenValue = currentValue
                    bestMove = move

        executionTime = time() - startTime
        return bestMove

    def min(self, board: Board.Board, depth: int) -> Union[float, int]:
        if depth == 0:
            return self.boardEvaluator.evaluate(board, depth)
        lowestSeenValue: float = float('inf')
        for move in board.currentPlayer.legalMoves:
            moveTransition: MoveTransition.MoveTransition = board.currentPlayer.makeMove(move)
            if moveTransition.moveStatus.isDone():
                currentValue = self.max(moveTransition.transitionBoard, depth-1)
                if currentValue <= lowestSeenValue:
                    lowestSeenValue = currentValue
        return lowestSeenValue

    def max(self, board: Board.Board, depth: int) -> Union[float, int]:
        if depth == 0:
            return self.boardEvaluator.evaluate(board, depth)
        highestSeenValue: float = float('-inf')
        for move in board.currentPlayer.legalMoves:
            moveTransition: MoveTransition.MoveTransition = board.currentPlayer.makeMove(move)
            if moveTransition.moveStatus.isDone():
                currentValue: int = self.min(moveTransition.transitionBoard, depth - 1)
                if currentValue >= highestSeenValue:
                    highestSeenValue = currentValue
        return highestSeenValue
