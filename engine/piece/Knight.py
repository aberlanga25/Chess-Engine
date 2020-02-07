from engine.piece.Piece import Piece
from engine.board import BoardUtils
from engine.board.Move import MajorMove, AttackMove
from typing import List

from engine.piece.PieceType import PieceType


class Knight(Piece):
    
    _moves = [-17, -15, -10, -6, 6, 10, 15, 17]
    
    def __init__(self, pieceCoordinate, alliance):
        super().__init__(pieceCoordinate, alliance)
        self._pieceType = PieceType.KNIGHT
    
    def calculateLegalMoves(self, board) -> List:
        legalMoves = []
        for moveOffset in self._moves:
            destinationCand = moveOffset + self.piecePosition
            if self.firstColumnExclusion(self.piecePosition, moveOffset) or self.secondColumnExclusion(self.piecePosition, moveOffset) \
                    or self.thirdColumnExclusion(self.piecePosition, moveOffset) or self.forthColumnExclusion(self.piecePosition, moveOffset):
                continue
            if BoardUtils.isValidTileCoordinate(destinationCand):
                candidTile = board.tile(destinationCand)
                if not candidTile.isTileOccupied():
                    legalMoves.append(MajorMove(board, self, destinationCand))
                else:
                    pieceAtDestination = candidTile.pieceOnTile
                    pieceAtDestAlliance = pieceAtDestination.pieceAlliance
                    if pieceAtDestAlliance != self.pieceAlliance:
                        legalMoves.append(AttackMove(board, self, destinationCand, pieceAtDestination))
        return legalMoves


    @staticmethod
    def firstColumnExclusion(coordinate, future) -> bool:
        return BoardUtils.inFirstColumn(coordinate) and (
                    future == 15 or future == -17 or future == -10 or future == 6)

    @staticmethod
    def secondColumnExclusion(coordinate, future) -> bool:
        return BoardUtils.inSecondColumn(coordinate) and (future == -10 or future == 6)

    @staticmethod
    def thirdColumnExclusion(coordinate, future) -> bool:
        return BoardUtils.inSevenColumn(coordinate) and (future == 10 or future == -6)

    @staticmethod
    def forthColumnExclusion(coordinate, future) -> bool:
        return BoardUtils.inEightColumn(coordinate) and (future == -15 or future == -6)

    def movePiece(self, move):
        return Knight(move.destinationCoordinate, move.movedPiece.pieceAlliance)