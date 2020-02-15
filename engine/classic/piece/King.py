from typing import List

from engine.classic.board import BoardUtils
from engine.classic.board.Move import MajorMove, AttackMove
from engine.classic.piece.Piece import Piece
from engine.classic.piece.PieceType import PieceType


class King(Piece):

    _moves = [-9, -8, -7, -1, 1, 7, 8, 9]

    def __init__(self, piecePosition, pieceAlliance):
        super().__init__(piecePosition, pieceAlliance)
        self._pieceType = PieceType.KING
        self._isCastled = False

    @property
    def isCastled(self):
        return self._isCastled

    def setCastled(self, option):
        self._isCastled = option

    def calculateLegalMoves(self, board) -> List:
        legalMoves = []

        for candidOffset in self._moves:
            if self.firstColumnExclusion(self.piecePosition, candidOffset) or self.eightColumnExclusion(self.piecePosition, candidOffset):
                continue
            candidDest = self.piecePosition + candidOffset
            if BoardUtils.isValidTileCoordinate(candidDest):
                candidTile = board.tile(candidDest)
                if not candidTile.isTileOccupied():
                    legalMoves.append(MajorMove(board, self, candidDest))
                else:
                    pieceAtDestination = candidTile.pieceOnTile
                    pieceAtDestAlliance = pieceAtDestination.pieceAlliance
                    if pieceAtDestAlliance != self.pieceAlliance:
                        legalMoves.append(AttackMove(board, self, candidDest, pieceAtDestination))

        return legalMoves

    @staticmethod
    def firstColumnExclusion(coordinate, future):
        return BoardUtils.inFirstColumn(coordinate) and (future == -9 or future == -1 or future == 7)

    @staticmethod
    def eightColumnExclusion(coordinate, future):
        return BoardUtils.inEightColumn(coordinate) and (future == -7 or future == 1 or future == 9)

    def movePiece(self, move):
        return King(move.destinationCoordinate, move.movedPiece.pieceAlliance)