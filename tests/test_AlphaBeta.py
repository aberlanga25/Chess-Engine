from unittest import TestCase
from engine.classic.board.Board import BoardBuilder
from engine.classic.board.Move import MoveFactory
from engine.classic.board.BoardUtils import *
from engine.classic.player.ai.AlphaBeta import AlphaBeta
from engine.classic.piece.Pawn import Pawn
from engine.classic.piece.King import King
from engine.classic.piece.Bishop import Bishop
from engine.classic.piece.Knight import Knight
from engine.classic.piece.Rook import Rook
from engine.classic.piece.Queen import Queen
from engine.classic.player.Alliance import Alliance
from pgn.FenUtils import createGameFromFen


class TestAlphaBeta(TestCase):

    def testOpeningDepth4BlackFirst(self):
        builder = BoardBuilder()

        # Black
        builder.setPiece(Rook(0, Alliance.Black))
        builder.setPiece(Knight(1, Alliance.Black))
        builder.setPiece(Bishop(2, Alliance.Black))
        builder.setPiece(Queen(3, Alliance.Black))
        builder.setPiece(King(4, Alliance.Black))
        builder.setPiece(Bishop(5, Alliance.Black))
        builder.setPiece(Knight(6, Alliance.Black))
        builder.setPiece(Rook(7, Alliance.Black))
        builder.setPiece(Pawn(8, Alliance.Black))
        builder.setPiece(Pawn(9, Alliance.Black))
        builder.setPiece(Pawn(10, Alliance.Black))
        builder.setPiece(Pawn(11, Alliance.Black))
        builder.setPiece(Pawn(12, Alliance.Black))
        builder.setPiece(Pawn(13, Alliance.Black))
        builder.setPiece(Pawn(14, Alliance.Black))
        builder.setPiece(Pawn(15, Alliance.Black))

        # White
        builder.setPiece(Rook(56, Alliance.White))
        builder.setPiece(Knight(57, Alliance.White))
        builder.setPiece(Bishop(58, Alliance.White))
        builder.setPiece(Queen(59, Alliance.White))
        builder.setPiece(King(60, Alliance.White))
        builder.setPiece(Bishop(61, Alliance.White))
        builder.setPiece(Knight(62, Alliance.White))
        builder.setPiece(Rook(63, Alliance.White))
        builder.setPiece(Pawn(48, Alliance.White))
        builder.setPiece(Pawn(49, Alliance.White))
        builder.setPiece(Pawn(50, Alliance.White))
        builder.setPiece(Pawn(51, Alliance.White))
        builder.setPiece(Pawn(52, Alliance.White))
        builder.setPiece(Pawn(53, Alliance.White))
        builder.setPiece(Pawn(54, Alliance.White))
        builder.setPiece(Pawn(55, Alliance.White))

        builder.setMoveMaker(Alliance.Black)

        board = builder.build()

        alphaBeta = AlphaBeta(4, 3)
        bestMove = alphaBeta.execute(board)

        self.assertEqual(bestMove, MoveFactory.createMove(
            board, getCoordinateAtPosition("e7"), getCoordinateAtPosition("e6")))

    def testadavancedLevelProblem2NakamuraShirov(self):
        builder = BoardBuilder()

        builder.setPiece(King(5, Alliance.Black))
        builder.setPiece(Pawn(10, Alliance.Black))
        builder.setPiece(Rook(25, Alliance.Black))
        builder.setPiece(Bishop(29, Alliance.Black))

        builder.setPiece(Knight(27, Alliance.White))
        builder.setPiece(Rook(36, Alliance.White))
        builder.setPiece(Pawn(39, Alliance.White))
        builder.setPiece(King(42, Alliance.White))
        builder.setPiece(Pawn(46, Alliance.White))

        builder.setMoveMaker(Alliance.White)

        board = builder.build()
        alphabeta = AlphaBeta(6, 5)
        bestMove = alphabeta.execute(board)

        self.assertEqual(bestMove, MoveFactory.createMove(
            board, getCoordinateAtPosition("d5"), getCoordinateAtPosition("c7")))

    def testQualityDepth6(self):
        board = createGameFromFen("8/6pk/pB5p/P7/2q4P/2b2QP1/5PK1/8 w - -")
        alphabeta = AlphaBeta(6, 2)
        bestMove = alphabeta.execute(board)
        print(bestMove)

        #self.assertEqual(bestMove, MoveFactory.createMove(
            #board, getCoordinateAtPosition("f7"), getCoordinateAtPosition("e7")))

    def testQuality2Depth6(self):
        board = createGameFromFen("6k1/3b3r/1p1p4/p1n2p2/1PPNpP1q/P3Q1p1/1R1RB1P1/5K2 b - - 0-1")
        alphabeta = AlphaBeta(6, 5)
        bestMove = alphabeta.execute(board)

        self.assertEqual(bestMove, MoveFactory.createMove(
            board, getCoordinateAtPosition("f7"), getCoordinateAtPosition("e7")))