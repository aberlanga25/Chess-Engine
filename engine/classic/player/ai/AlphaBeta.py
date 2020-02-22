from engine.classic.player.ai.MoveStrategy import MoveStrategy
from engine.classic.board import MoveTransition, Board, Move
from engine.classic.board.BoardUtils import *
from engine.classic.board.Move import nullMove
from engine.classic.board.MoveUtils import MoveSorter
from engine.classic.player.ai.StandardBoardEvaluator import StandardBoardEvaluator

from typing import *


class AlphaBeta(MoveStrategy):
    def __init__(self, depth: int, quiescenceFactor: int):
        self.evaluator = StandardBoardEvaluator()
        self.depth = depth
        self.quiescenceFactor = quiescenceFactor
        self.moveSorter = MoveSorter()
        self.boardsEvaluated = 0
        self.quiesceCount = 0
        self.cutOffsProduced = 0

    def __str__(self):
        return "AB+MO"

    @property
    def getNumBoardsEval(self):
        return self.boardsEvaluated

    def execute(self, board: Board.Board) -> Move.Move:
        currentPlayer = board.currentPlayer
        alliance = currentPlayer.alliance

        bestMove = nullMove
        highestSeenValue = -999999
        lowestSeenValue = 999999
        moveCounter = 1

        print(str(board.currentPlayer) + " THINKING with depth = " + str(self.depth))
        unsorted = board.currentPlayer.legalMoves
        for move in self.moveSorter.sort(unsorted):
            moveTransition = board.currentPlayer.makeMove(move)
            self.quiesceCount = 0
            if moveTransition.moveStatus.isDone():
                if board.currentPlayer.alliance.isWhite():
                    currentValue = self.min(
                        moveTransition.transitionBoard, self.depth - 1, highestSeenValue, lowestSeenValue)
                else:
                    currentValue = self.max(
                        moveTransition.transitionBoard, self.depth - 1, highestSeenValue, lowestSeenValue)
                if alliance.isWhite() and currentValue > highestSeenValue:
                    highestSeenValue = currentValue
                    bestMove = move
                elif alliance.isBlack() and currentValue < lowestSeenValue:
                    lowestSeenValue = currentValue
                    bestMove = move
            moveCounter += 1
        return bestMove

    def min(self, board: Board.Board, depth: int, highest: int, lowest: int) -> Union[float, int]:
        if depth == 0 or isEndGame(board):
            self.boardsEvaluated += 1
            return self.evaluator.evaluate(board, depth)

        currentLowest = lowest
        sortedList = self.moveSorter.sort(board.currentPlayer.legalMoves)
        for move in sortedList:
            moveTransition: MoveTransition.MoveTransition = board.currentPlayer.makeMove(move)
            if moveTransition.moveStatus.isDone():
                currentLowest = min(
                    [currentLowest, self.max(moveTransition.transitionBoard, depth-1, highest, currentLowest)])
                if currentLowest <= highest:
                    self.cutOffsProduced += 1
                    break
        return currentLowest

    def max(self, board: Board.Board, depth: int, highest: int, lowest: int) -> Union[float, int]:
        if depth == 0 or isEndGame(board):
            self.boardsEvaluated += 1
            return self.evaluator.evaluate(board, depth)

        currentHighest = highest
        unsorted = board.currentPlayer.legalMoves
        for move in self.moveSorter.sort(unsorted):
            moveTransition: MoveTransition.MoveTransition = board.currentPlayer.makeMove(move)
            if moveTransition.moveStatus.isDone():
                currentHighest = max(
                    [currentHighest, self.min(moveTransition.transitionBoard, depth - 1, currentHighest, lowest)])
                if lowest <= currentHighest:
                    self.cutOffsProduced += 1
                    break
        return currentHighest
