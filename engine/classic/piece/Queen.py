from engine.classic.piece.Piece import Piece
from engine.classic.board import BoardUtils
from engine.classic.board.Move import MajorMove, AttackMove
from typing import List

from engine.classic.piece.PieceType import PieceType


class Queen(Piece):

    _moves = [-9, -8, -7, -1, 1, 7, 8, 9]

    def __init__(self, piecePosition, pieceAlliance):
        super().__init__(piecePosition, pieceAlliance)
        self._pieceType = PieceType.QUEEN

    def calculateLegalMoves(self, board) -> List:

        legalMoves = []

        for candidOffset in self._moves:
            candidDestination: int = self.piecePosition

            while True:
                if self.firstColumnExclusion(candidDestination, candidOffset) or\
                        self.eightColumnExclusion(candidDestination, candidOffset):
                    break
                candidDestination += candidOffset
                if not BoardUtils.isValidTileCoordinate(candidDestination):
                    break
                else:
                    candidTile = board.tile(candidDestination)
                    if not candidTile.isTileOccupied():
                        legalMoves.append(MajorMove(board, self, candidDestination))
                    else:
                        pieceAtDestination = candidTile.pieceOnTile
                        pieceAtDestAlliance = pieceAtDestination.pieceAlliance
                        if pieceAtDestAlliance != self.pieceAlliance:
                            legalMoves.append(AttackMove(board, self, candidDestination, pieceAtDestination))
                        break

        return legalMoves

    @staticmethod
    def firstColumnExclusion(coordinate, future) -> bool:
        return BoardUtils.inFirstColumn(coordinate) and (future == -9 or future == -1 or future == 7)

    @staticmethod
    def eightColumnExclusion(coordinate, future) -> bool:
        return BoardUtils.inEightColumn(coordinate) and (future == -7 or future == 1 or future == 9)

    def movePiece(self, move):
        return Queen(move.destinationCoordinate, move.movedPiece.pieceAlliance)