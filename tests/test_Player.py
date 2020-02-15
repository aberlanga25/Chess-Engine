from unittest import TestCase

from engine.classic.board.Board import createStandardBoard, BoardBuilder
from engine.classic.board.Move import MoveFactory
from engine.classic.board.BoardUtils import *
from engine.classic.piece.King import King
from engine.classic.piece.Rook import Rook
from engine.classic.piece.Bishop import Bishop
from engine.classic.player.Alliance import Alliance
from engine.classic.player.ai.StandardBoardEvaluator import StandardBoardEvaluator


class TestPlayer(TestCase):

    def testSimpleEvaluation(self):
        board = createStandardBoard()
        t1 = board.currentPlayer.makeMove(
            MoveFactory.createMove(board, getCoordinateAtPosition("e2"), getCoordinateAtPosition("e4")))
        self.assertTrue(t1.moveStatus.isDone())
        t2 = t1.transitionBoard.currentPlayer.makeMove(
            MoveFactory.createMove(t1.transitionBoard, getCoordinateAtPosition("e7"), getCoordinateAtPosition("e5")))
        self.assertTrue(t2.moveStatus.isDone())
        standar = StandardBoardEvaluator()
        self.assertEqual(standar.evaluate(t2.transitionBoard, 0), 0)

    def testBug(self):
        board = createStandardBoard()
        t1 = board.currentPlayer.makeMove(
            MoveFactory.createMove(board, getCoordinateAtPosition("c2"), getCoordinateAtPosition("c3")))
        self.assertTrue(t1.moveStatus.isDone(), "First Move")
        t2 = t1.transitionBoard.currentPlayer.makeMove(
            MoveFactory.createMove(t1.transitionBoard, getCoordinateAtPosition("b8"), getCoordinateAtPosition("a6")))
        self.assertTrue(t2.moveStatus.isDone())
        t3 = t2.transitionBoard.currentPlayer.makeMove(
            MoveFactory.createMove(t2.transitionBoard, getCoordinateAtPosition("d1"), getCoordinateAtPosition("a4")))
        self.assertTrue(t3.moveStatus.isDone())
        t4 = t3.transitionBoard.currentPlayer.makeMove(
            MoveFactory.createMove(t3.transitionBoard, getCoordinateAtPosition("d7"), getCoordinateAtPosition("d6")))
        self.assertFalse(t4.moveStatus.isDone())

    def testDiscoveredCheck(self):
        builder = BoardBuilder()
        builder.setPiece(King(4, Alliance.Black))
        builder.setPiece(Rook(24, Alliance.Black))
        builder.setPiece(Bishop(44, Alliance.White))
        builder.setPiece(Rook(52, Alliance.White))
        builder.setPiece(King(58, Alliance.White))

        builder.setMoveMaker(Alliance.White)

        board = builder.build()
        t1 = board.currentPlayer.makeMove(
            MoveFactory.createMove(board, getCoordinateAtPosition("e3"), getCoordinateAtPosition("b6")))
        self.assertTrue(t1.moveStatus.isDone())
        self.assertTrue(t1.transitionBoard.currentPlayer.isInCheck)
        t2 = t1.transitionBoard.currentPlayer.makeMove(
            MoveFactory.createMove(t1.transitionBoard, getCoordinateAtPosition("a5"), getCoordinateAtPosition("b5")))
        self.assertFalse(t2.moveStatus.isDone())
        t3 = t2.transitionBoard.currentPlayer.makeMove(
            MoveFactory.createMove(t2.transitionBoard, getCoordinateAtPosition("a5"), getCoordinateAtPosition("e5")))
        self.assertTrue(t3.moveStatus.isDone())

    def testIllegalMove(self):
        board = createStandardBoard()
        m1 = MoveFactory.createMove(board, getCoordinateAtPosition("e2"), getCoordinateAtPosition("e6"))
        t1 = board.currentPlayer.makeMove(m1)
        self.assertFalse(t1.moveStatus.isDone())