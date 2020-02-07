from typing import *

from engine.player.Alliance import Alliance
from engine.player.BlackPlayer import BlackPlayer
from engine.player.WhitePlayer import WhitePlayer
from engine.player import Player
from engine.board.Tile import createTile, _Tile
from engine.piece.Pawn import Pawn
from engine.piece.King import King
from engine.piece.Bishop import Bishop
from engine.piece.Knight import Knight
from engine.piece.Rook import Rook
from engine.piece.Queen import Queen


class BoardBuilder:

    def __init__(self):
        self.boardConfig = {}
        self.moveMaker: Alliance = Alliance.White
        self.enpassantPawn = None

    def setPiece(self, piece):
        self.boardConfig[piece.piecePosition] = piece
        return self

    def setMoveMaker(self, nextMoveMaker):
        self.moveMaker = nextMoveMaker
        return self

    def build(self):
        return Board(self)

    def setEnPassantPawn(self, movedPawn):
        self.enpassantPawn = movedPawn


@final
class Board(object):
    _gameboard: list
    whitePieces: list
    blackPieces: list

    def __init__(self, builder):
        self._gameboard = self.createGameBoard(builder)
        self.whitePieces = self.calculateActivePieces(self._gameboard, Alliance.White)
        self.blackPieces = self.calculateActivePieces(self._gameboard, Alliance.Black)
        self.enPassantPawn = builder.enpassantPawn
        self.whiteStandardLegalMoves = self.calculateLegalMoves(self.whitePieces)
        self.blackStandardLegalMoves = self.calculateLegalMoves(self.blackPieces)
        self.whitePlayer: Player.Player = WhitePlayer(self, self.whiteStandardLegalMoves, self.blackStandardLegalMoves)
        self.blackPlayer: Player.Player = BlackPlayer(self, self.whiteStandardLegalMoves, self.blackStandardLegalMoves)
        self.currentPlayer: Player.Player = builder.moveMaker.choosePlayer(self.whitePlayer, self.blackPlayer)

    def __str__(self):
        string = ""
        for i in range(64):
            tileText = str(self._gameboard[i])
            string += tileText + " "
            if (i + 1) % 8 == 0:
                string += "\n"
        return string

    def tile(self, coordinate) -> _Tile:
        return self._gameboard[coordinate]

    @property
    def allLegalMoves(self):
        return self.blackPlayer.legalMoves +self.whitePlayer.legalMoves

    @staticmethod
    def createGameBoard(builder: BoardBuilder) -> list:
        tile = []
        for i in range(64):
            tile.append(createTile(i, builder.boardConfig.get(i)))
        return tile

    @staticmethod
    def calculateActivePieces(gameboard, alliance) -> list:
        activePieces = []
        for tile in gameboard:
            if tile.isTileOccupied():
                piece = tile.pieceOnTile
                if piece.pieceAlliance == alliance:
                    activePieces.append(piece)
        return activePieces

    def calculateLegalMoves(self, pieces) -> List:
        legalMoves = []
        for piece in pieces:
            legalMoves += piece.calculateLegalMoves(self)
        return legalMoves


def createStandardBoard():
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

    builder.setMoveMaker(Alliance.White)

    return builder.build()
