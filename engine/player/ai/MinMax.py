from engine.player.ai.MoveStrategy import MoveStrategy
from engine.player.ai.StandardBoardEvaluator import StandardBoardEvaluator
from engine.board import Board
from engine.board import Move, MoveTransition
from engine.board.BoardUtils import *

from typing import *
from time import time
from atomicl import AtomicLong


class MinMax(MoveStrategy):

    def __init__(self, depth: int):
        self.boardEvaluator = StandardBoardEvaluator()
        self.depth: int = depth
        self._boardsEvaluated = 0

    def __str__(self):
        return "MiniMax"

    @property
    def boardsEvaluated(self):
        return self._boardsEvaluated

    def execute(self, board: Board.Board) -> Move.Move:
        startTime: float = time()
        bestMove: Move.Move = Move.nullMove
        highestSeenValue = float('-inf')
        lowestSeenValue = float('inf')

        print(str(board.currentPlayer) + " Thinking with Depth = " + str(self.depth))

        self.freqtable = []
        self.freqtableIndex = 0

        moveCounter = 1

        numMoves = len(board.currentPlayer.legalMoves)

        for move in board.currentPlayer.legalMoves:
            moveTransition = board.currentPlayer.makeMove(move)
            if moveTransition.moveStatus.isDone():
                row = FreqTableRow(move)
                self.freqtable.append(row)
                if board.currentPlayer.alliance.isWhite():
                    currentValue = self.min(moveTransition.transitionBoard, self.depth-1)
                else:
                    currentValue = self.max(moveTransition.transitionBoard, self.depth-1)
                print(str(self) + " analysing move (" + str(moveCounter) + "/" + str(numMoves) + ") " + str(move) + " scores "
                      + str(currentValue) + " " + str(row))
                self.freqtableIndex += 1
                if board.currentPlayer.alliance.isWhite() and currentValue >= highestSeenValue:
                    highestSeenValue = currentValue
                    bestMove = move
                elif board.currentPlayer.alliance.isBlack() and currentValue <= lowestSeenValue:
                    lowestSeenValue = currentValue
                    bestMove = move
            moveCounter += 1
        executionTime = time() - startTime

        return bestMove

    def min(self, board: Board.Board, depth: int) -> Union[float, int]:
        if depth == 0:
            self._boardsEvaluated += 1
            self.freqtable[self.freqtableIndex].increment()
            return self.boardEvaluator.evaluate(board, depth)

        if self.isEndGameScenario(board):
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
            self._boardsEvaluated += 1
            self.freqtable[self.freqtableIndex].increment()
            return self.boardEvaluator.evaluate(board, depth)

        if self.isEndGameScenario(board):
            return self.boardEvaluator.evaluate(board, depth)
        highestSeenValue: float = float('-inf')
        for move in board.currentPlayer.legalMoves:
            moveTransition: MoveTransition.MoveTransition = board.currentPlayer.makeMove(move)
            if moveTransition.moveStatus.isDone():
                currentValue: int = self.min(moveTransition.transitionBoard, depth - 1)
                if currentValue >= highestSeenValue:
                    highestSeenValue = currentValue
        return highestSeenValue

    @staticmethod
    def isEndGameScenario(board: Board.Board):
        return board.currentPlayer.isInCheckMate or board.currentPlayer.isInStaleMate


class FreqTableRow:
    def __init__(self, move: Move.Move):
        self._count = AtomicLong()
        self.move = move

    def __str__(self):
        return str(getPositionAtCoordinate(self.move.currentCoordinate)) + \
               str(getPositionAtCoordinate(self.move.destinationCoordinate)) + " : " + str(self.count)

    @property
    def count(self):
        return self._count.value

    def increment(self):
        self._count.get_and_set(self._count.value + 1)
