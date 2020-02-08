from unittest import TestCase
from engine.board.Board import createStandardBoard
from engine.board.Move import MoveFactory
from engine.board.BoardUtils import *
from engine.player.ai.MinMax import MinMax
from engine.player.ai.AlphaBeta import AlphaBeta


class TestBoard(TestCase):

    def testAI(self):
        board = createStandardBoard()
        moveStrategy = MinMax(3)
        move = moveStrategy.execute(board)
        print(move)

    def testFoolsMate(self):
        board = createStandardBoard()
        t1 = board.currentPlayer.makeMove(
            MoveFactory.createMove(board, getCoordinateAtPosition("f2"), getCoordinateAtPosition("f3")))
        self.assertTrue(t1.moveStatus.isDone())

        t2 = t1.transitionBoard.currentPlayer.makeMove(
            MoveFactory.createMove(t1.transitionBoard, getCoordinateAtPosition("e7"), getCoordinateAtPosition("e5")))
        self.assertTrue(t2.moveStatus.isDone())

        t3 = t2.transitionBoard.currentPlayer.makeMove(
            MoveFactory.createMove(t2.transitionBoard, getCoordinateAtPosition("g2"), getCoordinateAtPosition("g4")))
        self.assertTrue(t3.moveStatus.isDone(), "3 move")

        ai = AlphaBeta(3,3)
        aiMove = ai.execute(t3.transitionBoard)

        bestMove = MoveFactory.createMove(t3.transitionBoard,  getCoordinateAtPosition("d8"), getCoordinateAtPosition("h4"))

        self.assertEqual(aiMove, bestMove)
