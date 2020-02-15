from engine.classic.board import BoardUtils, Move
from engine.classic.piece.Piece import Piece
from typing import List

from engine.classic.piece.PieceType import PieceType


class Rook(Piece):

    _moves = [-8, -1, 1, 8]

    def __init__(self, piecePosition, pieceAlliance):
        super().__init__(piecePosition, pieceAlliance)
        self._pieceType = PieceType.ROOK

    def calculateLegalMoves(self, board) -> List:

        legalMoves = []

        for candidOffset in self._moves:
            candidDestination: int = self.piecePosition

            while BoardUtils.isValidTileCoordinate(candidDestination):
                candidDestination += candidOffset
                if self.firstColumnExclusion(candidDestination, candidOffset) or\
                        self.eightColumnExclusion(candidDestination, candidOffset):
                    break
                if BoardUtils.isValidTileCoordinate(candidDestination):
                    candidTile = board.tile(candidDestination)
                    if not candidTile.isTileOccupied():
                        legalMoves.append(Move.MajorMove(board, self, candidDestination))
                    else:
                        pieceAtDestination = candidTile.pieceOnTile
                        pieceAtDestAlliance = pieceAtDestination.pieceAlliance
                        if pieceAtDestAlliance != self.pieceAlliance:
                            legalMoves.append(Move.AttackMove(board, self, candidDestination, pieceAtDestination))
                        break

        return legalMoves

    @staticmethod
    def firstColumnExclusion(coordinate, future) -> bool:
        return BoardUtils.inFourColumn(coordinate) and (future == -1)

    @staticmethod
    def eightColumnExclusion(coordinate, future) -> bool:
        return BoardUtils.inEightColumn(coordinate) and (future == 1)

    def movePiece(self, move):
        return Rook(move.destinationCoordinate, move.movedPiece.pieceAlliance)
