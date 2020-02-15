import asyncio
from queue import SimpleQueue
from typing import *

from engine.classic.player.ai.MoveStrategy import MoveStrategy
from engine.classic.board import MoveTransition, Board, Move
from engine.classic.board.BoardUtils import *
from engine.classic.player.ai.StandardBoardEvaluator import StandardBoardEvaluator


class ParallelMiniMax(MoveStrategy):

    def __init__(self, depth: int):
        self.boardEvaluator = StandardBoardEvaluator()
        self.depth: int = depth
        self._boardsEvaluated = 0
        self.thread = 0

    def __str__(self):
        return "MiniMax"

    @property
    def boardsEvaluated(self):
        return self._boardsEvaluated

    def execute(self, board: Board.Board) -> None:
        bestMove: Move.Move = Move.nullMove
        highestSeenValue = float('-inf')
        lowestSeenValue = float('inf')

        print(str(board.currentPlayer) + " Thinking with Depth = " + str(self.depth))

        loop = asyncio.get_event_loop()
        tasks = [self.createAlg(board, move) for move in board.allLegalMoves]
        loop.run_until_complete(asyncio.wait(tasks))
        loop.close()

    async def createAlg(self, board, move):
        print("Start ", move)
        moveTransition = board.currentPlayer.makeMove(move)

        if moveTransition.moveStatus.isDone():
            if board.currentPlayer.alliance.isWhite():
                #print("Depth is ", self.depth)
                queue = SimpleQueue()
                await self.min(moveTransition.transitionBoard, self.depth - 1, queue)

            else:
                #print("Depth is ", self.depth)
                queue = SimpleQueue()
                await self.max(moveTransition.transitionBoard, self.depth - 1, queue)
        print(queue.get())

    async def min(self, board: Board.Board, depth: int, queue: SimpleQueue) -> None:
        if depth == 0 or self.isEndGameScenario(board):
            queue.put(self.boardEvaluator.evaluate(board, depth))
            return
        lowestSeenValue: float = float('inf')
        await asyncio.sleep(0.00001)
        for move in board.currentPlayer.legalMoves:
            moveTransition: MoveTransition.MoveTransition = board.currentPlayer.makeMove(move)
            if moveTransition.moveStatus.isDone():
                await self.max(moveTransition.transitionBoard, depth-1, queue)
                currentValue = queue.get()
                if currentValue <= lowestSeenValue:
                    lowestSeenValue = currentValue
        queue.put(lowestSeenValue)
        return

    async def max(self, board: Board.Board, depth: int, queue: SimpleQueue) -> None:
        if depth == 0 or self.isEndGameScenario(board):
            queue.put(self.boardEvaluator.evaluate(board, depth))
            return

        highestSeenValue: float = float('-inf')
        await asyncio.sleep(0.00001)
        for move in board.currentPlayer.legalMoves:
            moveTransition: MoveTransition.MoveTransition = board.currentPlayer.makeMove(move)
            if moveTransition.moveStatus.isDone():
                await self.min(moveTransition.transitionBoard, depth-1, queue)
                currentValue = queue.get()
                if currentValue >= highestSeenValue:
                    highestSeenValue = currentValue
        queue.put(highestSeenValue)
        return

    @staticmethod
    def isEndGameScenario(board: Board.Board):
        return board.currentPlayer.isInCheckMate or board.currentPlayer.isInStaleMate
